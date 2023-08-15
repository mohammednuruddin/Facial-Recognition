import database
import os
import datetime
import time
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title('Attendance Register')

        self.background = ImageTk.PhotoImage(file='images/frontend.jpg')
        self.start_image = ImageTk.PhotoImage(file='images/start.png')
        self.export_image = ImageTk.PhotoImage(file='images/export.png')
        self.help_image = ImageTk.PhotoImage(file='images/help.png')
        self.exit_image = ImageTk.PhotoImage(file= 'images/exit.png')
        self.info_image = ImageTk.PhotoImage(file='images/info.png')
        self.open_image = ImageTk.PhotoImage(file='images/open.png')

        self.back = Label(self.root, image=self.background).pack()

        self.start_button = Button(self.root, image=self.start_image, relief='flat', background='white',
                                   cursor='hand2', borderwidth=0, activebackground='white', command=database.main)
        self.start_button.place(x=405, y=195)

        self.export_button = Button(self.root, image=self.export_image, relief='flat', background='white',
                                    cursor='hand2', borderwidth=0, activebackground='white', command=self.export)
        self.export_button.place(x=675, y=195)

        self.info_button = Button(self.root, image=self.info_image, relief='flat', background='white',
                                  cursor='hand2', borderwidth=0, activebackground='white', command=self.info)
        self.info_button.place(x=405, y=310)

        self.help_button = Button(self.root, image=self.help_image, relief='flat', background='white',
                                  cursor='hand2', borderwidth=0, activebackground='white', command=self.help)
        self.help_button.place(x=585, y=310)

        self.open_button = Button(self.root, image=self.open_image, relief='flat', background='white',
                                  cursor='hand2', borderwidth=0, activebackground='white', command=self.open_file)
        self.open_button.place(x=765, y=310)

        self.exit_button = Button(self.root, image=self.exit_image, relief='flat', background='white',
                                  cursor='hand2', borderwidth=0, activebackground='white', command=self.exit)
        self.exit_button.place(x=585, y=410)

        self.time_show = Label(self.root, bg='white', foreground='#f9c439')
        self.time_show.place(x=470, y=620)

        def ticking():
            now = datetime.datetime.now()
            today = '{:%B %d, %y}'.format(now)
            current_time = time.strftime('%I:%M:%S%p')

            self.time_show.config(text=f'{today}\t{current_time}', font=('arial', 20, 'bold'))

            self.time_show.after(1, ticking)

        ticking()

    def export(self):
        prompt = messagebox.askquestion('export', 'Export attendance to CSV file?')
        if prompt == 'yes':
            database.add_to_csv()
        else:
            p = messagebox.askquestion(message='Attendance data will be lost. Continue?')
            if p == 'yes':
                pass
            else:
                self.export()

    def exit(self):
        prompt = messagebox.askquestion('exit', 'Unexported attendance will be lost\n'
                                                'Do you want to quit (No crying afterwards)?')
        if prompt == 'yes':
            self.root.destroy()

    def help(self):
        messagebox.showinfo('help', "1. After you have finished recording attendance, press 'q' to close."
                                    "\n2. Click 'export' after recording to save records in an 'attendance.csv' file"
                                    "\n3. Make sure to export attendance before closing, else no crying afterwards"
                                    "\n4. Click 'info' to show information of records"
                                    "\n5. Click 'open' to open the csv records file"
                                    "\n6. Close all other windows before returning to home screen")

    def info(self):
        number_of_students = len(database.attended)
        if number_of_students == 1:
            messagebox.showinfo('info', 'One person recorded')
        else:
            messagebox.showinfo('info', f'{number_of_students} people recorded.')

    def open_file(self):
        os.system('cmd /c "attendance.csv"')


if __name__ == '__main__':
    root = Tk()
    root.geometry('1360x720')
    root.resizable(False, False)
    application = Gui(root)
    root.mainloop()
