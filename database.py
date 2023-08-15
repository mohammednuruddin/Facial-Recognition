import cv2
import face_recognition
import os
import sqlite3
from peewee import *
from csv import *
from PIL import Image

db = SqliteDatabase('student.db')

class_names = []
images = []
my_list = os.listdir('/data')
attended = []
database_records = []

for item in my_list:
    images.append(cv2.imread(f'data/{item}'))
    class_names.append(os.path.splitext(item)[0])


def run_query(query, parameter=()):
    with sqlite3.connect('student.db') as connection:
        cursor = connection.cursor()
        query_result = cursor.execute(query, parameter)
        connection.commit()
    return query_result


def find_encodings():
    encodings = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        known_faces_encoding = face_recognition.face_encodings(image)[0]
        encodings.append(known_faces_encoding)
    return encodings


def add_to_csv():
    query = 'select * from students'
    records = run_query(query)
    with open('attendance.csv', 'w', newline='') as csv_file:
        fieldnames = ['Id', 'Present']
        id_writer = DictWriter(csv_file, fieldnames=fieldnames)
        id_writer.writeheader()

        for record in records:
            id_writer.writerow({
                'Id': record[0],
                'Present': record[1]
            })


class Students(Model):
    id = CharField(max_length=15, unique=True)
    present = IntegerField(default=0)

    class Meta:
        database = db


students_list = []


def add_records():
    for i in class_names:
        student_list = [
            {'id': i, 'present': 0}
        ]
        for student in student_list:
            try:
                Students.create(id=student['id'], present=student['present'])
            except IntegrityError:
                student_records = Students.get(id=student['id'])
                student_records.present = 0
                student_records.save()

            students_list.append(student['id'])


def update_records():
    for student in students_list:
        if student in attended:
            try:
                Students.create(id=student, present=1)
            except IntegrityError:
                student_record = Students.get(id=student)
                student_record.present = 1
                student_record.save()


def main():
    video_capture = cv2.VideoCapture(0)

    known_faces_encodes = find_encodings()

    while True:
        success, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        resized_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        resized_converted = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        unknown_face_locations = face_recognition.face_locations(resized_converted)
        unknown_face_encodes = face_recognition.face_encodings(resized_converted, unknown_face_locations)

        for unknown_face, unknown_face_location in zip(unknown_face_encodes, unknown_face_locations):
            matches = face_recognition.compare_faces(known_faces_encodes, unknown_face)
            # face_distances = face_recognition.face_distance(known_faces_encodes, unknown_face)

            # match_index = np.argmin(face_distances)

            # if matches[match_index]:
            #    name = class_names[match_index]
            #    print(f'{name} was found')
            name = 'unknown'
            if True in matches:
                match_index = matches.index(True)
                name = class_names[match_index]
                if name not in attended:
                    attended.append(name)

            y1, x2, y2, x1 = unknown_face_location
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255))
            # cv2.rectangle(frame, (x1-10, y2-35), (x2, y2), (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1, y2+16), cv2.ADAPTIVE_THRESH_MEAN_C, 1, (255, 255, 255))

        cv2.imshow('Cam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

    try:
        db.connect()
        db.create_tables([Students], safe=True)

    except OperationalError:
        pass

    add_records()
    update_records()


if __name__ == '__main__':
    main()
    add_to_csv()
