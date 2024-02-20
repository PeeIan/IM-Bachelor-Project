from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from datetime import *
import time
import smtplib
import random
import PIL.Image
import base64
from tkinter import messagebox
from student_upd import Student
from face_recognition import Face_Recognition
from attendance import Attendance
from face_recognition import new_tcid
import pymongo
from pymongo import MongoClient

from lesson import Lesson
from import_csv import InsertData
from report_attendance import Report
from database_str import Database_str
import mysql.connector

value_from_p1 = None

def new_print(value):
    global value_from_p1
    value_from_p1 = value
    print(value_from_p1)



class Face_Recognition_System(Toplevel):
    def __init__(self, window):
        """takes window as arguments to show all the attributes and keep let them get advantage of the methods,
        that have been created to provide them various feature"""

        Toplevel.__init__(self)
        self.window = window
        self.geometry("1366x720+0+0")
        self.title("Student Attendance Management System")
        self.iconbitmap('ImageFaceDetect//gaming.ico')
        self.resizable(False, False)
        self.admin_dashboard_frame = ImageTk.PhotoImage\
            (file='ImageFaceDetect//admin_frame.png')
        self.image_panel = Label(self, image=self.admin_dashboard_frame)
        self.image_panel.pack(fill='both', expand='yes')

        new_tcid(value_from_p1)

        # thông tin kết nối database
        self.db = Database_str()

        self.txt = "Facial Recognition System"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self, text=self.txt, font=('times new roman', 20, "bold"), bg="white",
                             fg='black',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=470, y=33, width=550)
        # self.slider()
        # self.heading_color()

        # =========account===========
        # ===lấy thông tin tài khoản=============
        self.account = StringVar()
        self.p_password=StringVar()
        self.n_password=StringVar()
        self.c_password=StringVar()

        if (value_from_p1 == "0"):#Nếu thông tin truyền từ form login là 0 -> tài khoản admin
            self.account.set("admin")
        elif (value_from_p1 == None):#Nếu chạy riêng file main thì coi như tài khoản admin
            self.account.set("admin")
        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute("select Email from teacher where Teacher_id=%s", (
                    value_from_p1,
                ))
                row = my_cursor.fetchone()
                self.account.set(str(row[0]))
                # self.account = row[0]
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self)

        # ========================================================================
        # ============================Date and time==============================
        # ========================================================================
        self.clock_image = ImageTk.PhotoImage(file="ImageFaceDetect/time.png")
        self.date_time_image = Label(self, image=self.clock_image, bg="white")
        self.date_time_image.place(x=35, y=45)

        self.date_time = Label(self)
        self.date_time.place(x=65, y=35)
        self.time_running()

        # ========================================================================
        # ============================Current user================================
        # ========================================================================
        self.current_user_image = ImageTk.PhotoImage(file="ImageFaceDetect/current_user.png")
        self.current_user_label = Label(self, image=self.current_user_image, bg="white")
        self.current_user_label.place(x=1000, y=47)

        self.current_user = Label(self, bg="white",
                                  font=("times new roman", 10, "bold"), fg="green")
        self.current_user.place(x=1030, y=48)

        # ========================================================================
        # ============================Home button====================================
        # ========================================================================
        self.home = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\home.png')
        self.home_button = Button(self, image=self.home,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.click_home)

        self.home_button.place(x=43, y=113)
        self.click_home()

        # ========================================================================
        # ============================Manage button===============================
        # ========================================================================
        self.manage = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\manage.png')
        self.manage_button = Button(self, image=self.manage,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.click_manage)

        self.manage_button.place(x=41, y=233)

        # ========================================================================
        # ============================View button===============================
        # ========================================================================
        self.view = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\view.png')
        self.view_button = Button(self, image=self.view,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.face_recognition)
        self.view_button.place(x=41, y=353)

        # ========================================================================
        # ============================Setting button===============================
        # ========================================================================
        self.setting = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\setting.png')
        self.setting_button = Button(self, image=self.setting,
                                     font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                     , borderwidth=0, background="white", cursor="hand2", command=self.click_setting)
        self.setting_button.place(x=41, y=473)

        # ========================================================================
        # ============================Exit button===============================
        # ========================================================================
        self.exit = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\exit_button.png')
        self.exit_button = Button(self, image=self.exit,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.click_exit)
        self.exit_button.place(x=41, y=593)

        # ========================================================================
        # ============================Logout button===============================
        # ========================================================================
        self.logout = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\logout.png')
        self.logout_button = Button(self, image=self.logout,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.click_logout)
        self.logout_button.place(x=1241, y=50)



    def click_home(self):
        # ===========variable============
        self.student = StringVar()
        self.teacher = StringVar()
        self.classCount = StringVar()


        home_frame = Frame(self)
        home_frame.place(x=145, y=105, height=576, width=1181)

        self.home_dashboard_frame = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\home_frame.png')
        self.home_panel = Label(home_frame, image=self.home_dashboard_frame, bg="white")
        self.home_panel.pack(fill='both', expand='yes')

        try:
            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            collection = db["student"]
            count_student = collection.count_documents({})
            """
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            # ======== to==========
            my_cursor.execute("select count(*) from student")
            count_st = my_cursor.fetchone()
            """
            self.student.set(count_student)
            # =======attendance========
            collection = db["class"]
            count_class = collection.count_documents({})
            self.classCount.set(count_class)
            # =======đi muộn=============
            collection = db["teacher"]
            count_teacher = collection.count_documents({})
            self.teacher.set(count_teacher)
            # ========không điểm danh=======



        except BaseException as msg:
            print(msg)
        total_students = Label(home_frame, text=f" Total \n {self.student.get()}\n students",
                               font=("times new roman", 30, "bold"),
                               background="white", fg='#e67c0b')
        total_students.place(x=230, y=90)

        total_teacher = Label(home_frame, text=f" Total \n {self.teacher.get()}\n teachers",
                                font=("times new roman", 30, "bold"),
                                background="white", fg='#e67c0b')
        total_teacher.place(x=720, y=90)

        total_class = Label(home_frame, text=f" Total \n {self.classCount.get()}\n class",
                                 font=("times new roman", 30, "bold"),
                                 background="white", fg='#e67c0b')
        total_class.place(x=230, y=330)

        img_ex = PIL.Image.open(r"ImageFaceDetect\excel.png")
        img_student = img_ex.resize((90, 90), PIL.Image.ANTIALIAS)
        self.photoimgsv = ImageTk.PhotoImage(img_ex)


        self.ex_button = Button(home_frame, image=self.photoimgsv,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.excel_data)
        self.ex_button.place(x=670,y=310,width=260,height=180)

    def click_manage(self):
        """ opens new frame from where one can go to manage students, employees, departments, course, section
        and batch"""
        manage_frame = Frame(self, bg="white")
        manage_frame.place(x=145, y=105, height=576, width=1181)

        self.manage_dashboard_frame = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\manage_frame.png')
        self.manage_panel = Label(manage_frame, image=self.manage_dashboard_frame, bg="white")
        self.manage_panel.pack(fill='both', expand='yes')

        # =============Button================
        img_btn1 = Image.open(r"ImageFaceDetect\student2.png")
        img_btn1 = img_btn1.resize((60, 88), Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)

        button_student = Button(manage_frame, text="Student", font=("times new roman", 14, "bold"), command=self.student_details,
                    image=self.photobtn1, cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        button_student.place(x=340, y=117, width=127, height=127)

        #nút thống kê các bản điểm danh
        img_btn2 = Image.open(r"ImageFaceDetect\ghichu.png")
        img_btn2 = img_btn2.resize((60, 88), Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)

        button_att = Button(manage_frame, text="Attendance", font=("times new roman", 14, "bold"),
                                command=self.attendance_data,
                                image=self.photobtn2, cursor="hand2",
                                activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=725, y=117, width=127, height=127)

        #nút quản lý buổi học
        img_btn3 = Image.open(r"ImageFaceDetect\lesson.png")
        img_btn3 = img_btn3.resize((60, 88), Image.ANTIALIAS)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)

        button_att = Button(manage_frame, text="Class session", font=("times new roman", 14, "bold"),
                            command=self.lesson_data,
                            image=self.photobtn3, cursor="hand2",
                            activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=725, y=327, width=127, height=127)

        #nút thống kê hệ thống
        img_btn4 = Image.open(r"ImageFaceDetect\report.png")
        img_btn4 = img_btn4.resize((60, 88), Image.ANTIALIAS)
        self.photobtn4 = ImageTk.PhotoImage(img_btn4)

        button_att = Button(manage_frame, text="Statistics", font=("times new roman", 14, "bold"),
                            command=self.report_data,
                            image=self.photobtn4, cursor="hand2",
                            activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=340, y=327, width=127, height=127)







    def click_setting(self):
        """ Allows user to change their password using old password, validations, update entry data to database
        table containing that email or username is done in this method"""
        setting_frame = Frame(self, bg="white")
        setting_frame.place(x=145, y=105, height=576, width=1181)
        self.setting_dashboard_frame = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\setting_frame.png')
        self.setting_panel = Label(setting_frame, image=self.setting_dashboard_frame, bg="white")
        self.setting_panel.pack(fill='both', expand='yes')

        txt = "Change password"

        heading = Label(setting_frame, text=txt, font=('times new roman', 20, "bold"), bg="white",
                        fg='black',
                        bd=5,
                        relief=FLAT)
        heading.place(x=410, y=27, width=350)

        # ========================================================================
        # ============================Username====================================
        # ========================================================================

        self.username_label = Label(setting_frame, text="Account", bg="white", fg="#4f4e4d",
                                    font=("times new roman", 13, "bold"))
        self.username_label.place(x=415, y=90)
        # print(self.account)
        self.username_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.account,
                                    font=("times new roman ", 11),state="disabled",)
        self.username_entry.place(x=450, y=118, width=300)

        # ========================================================================
        # ============================PreviousPassword============================
        # ========================================================================

        self.p_password_label = Label(setting_frame, text="Old password", bg="white", fg="#4f4e4d",
                                      font=("times new roman", 13, "bold"))
        self.p_password_label.place(x=415, y=180)

        self.p_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.p_password,
                                      font=("times new roman ", 12), show='*')
        self.p_password_entry.place(x=450, y=207, width=300)  # trebuchet ms

        # ========================================================================
        # ============================New Password============================
        # ========================================================================

        self.n_password_label = Label(setting_frame, text="New password", bg="white", fg="#4f4e4d",
                                      font=("times new roman", 13, "bold"))
        self.n_password_label.place(x=415, y=270)

        self.n_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.n_password,
                                      font=("times new roman ", 12), show='*')
        self.n_password_entry.place(x=450, y=298, width=300)  # trebuchet ms

        # ========================================================================
        # ============================Confirm Password============================
        # ========================================================================

        self.c_password_label = Label(setting_frame, text="Confirm password", bg="white", fg="#4f4e4d",
                                      font=("times new roman", 13, "bold"))
        self.c_password_label.place(x=415, y=360)

        self.c_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.c_password,
                                      font=("times new roman ", 12), show='*')
        self.c_password_entry.place(x=450, y=388, width=300)  # trebuchet ms

        # ========================================================================
        # ============================Submit button================================
        # ========================================================================

        self.submit = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\submit.png')

        self.submit_button = Button(setting_frame, image=self.submit,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2",
                                    command=self.reset_pass)
        self.submit_button.place(x=520, y=450)

    def reset_pass(self):
        if self.p_password_entry.get()=="":
            messagebox.showerror("Error","Please enter your old password",parent=self)
        elif self.n_password_entry.get()=="":
            messagebox.showerror("Error","Please enter your new password",parent=self)
        elif self.c_password_entry.get()=="":
            messagebox.showerror("Error", "Please re-enter your password",parent=self)
        elif self.n_password_entry.get()!="" and self.n_password_entry.get()!=self.c_password_entry.get():
            messagebox.showerror("Error", "Please re-enter the password correctly", parent=self)
        elif self.p_password_entry.get()==self.n_password_entry.get():
            messagebox.showerror("Error", "The new password matches the new password", parent=self)
        else:
            if(self.username_entry.get()=="admin"):
                client = MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                admin_collection = db['admin']  # 替換為你的admin集合名稱

                row = admin_collection.find_one({"Account": self.username_entry.get()}, {"Password": 1, "_id": 0})
                print(row)
                if row and "Password" in row and row["Password"] != self.p_password_entry.get():
                    messagebox.showerror("Error", "Incorrect old password!!!", parent=self)
                else:

                    admin_collection.update_one(
                        {"Account": self.username_entry.get()},
                        {"$set": {"Password": self.n_password_entry.get()}}
                    )
                    messagebox.showinfo("Notification","Password changed successfully",parent=self)
                    self.p_password.set("")
                    self.n_password.set("")
                    self.c_password.set("")
            else:
                client = MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                teacher_collection = db["teacher"]
                row = teacher_collection.find_one({"Teacher_id": int(value_from_p1)}, {"Password": 1, "_id": 0})

                if row and "Password" in row and row["Password"] != self.p_password_entry.get():
                    messagebox.showerror("Error", "Incorrect old password !!!", parent=self)
                else:
                    teacher_collection.update_one(
                        {"Teacher_id": int(value_from_p1)},
                        {"$set": {"Password": self.n_password_entry.get()}}
                    )

                    messagebox.showinfo("Notification","Password changed successfully", parent=self)
                    self.p_password.set("")
                    self.n_password.set("")
                    self.c_password.set("")






    def face_recognition(self):
        self.new_window=Toplevel(self)
        self.app=Face_Recognition(self.new_window)
    def student_details(self):
        self.new_window=Toplevel(self)
        self.app=Student(self.new_window)
    def attendance_data(self):
        self.new_window=Toplevel(self)
        self.app=Attendance(self.new_window)

    def lesson_data(self):
        self.new_window = Toplevel(self)
        self.app = Lesson(self.new_window)
    def report_data(self):
        self.new_window=Toplevel(self)
        self.app=Report(self.new_window)

    def excel_data(self):
        self.new_window = Toplevel(self)
        self.app = InsertData(self.new_window)


    def click_exit(self):
        """ Allows user to terminates the program when chosen yes"""
        self.deiconify()
        ask = messagebox.askyesnocancel("Exit confirmation","Are you sure you want to close the program?", parent=self)
        if ask is True:
            self.quit()

    def click_logout(self):
        """Logouts the user to login page from where they will require password in order to login again"""
        Exit = messagebox.askyesno("Logout","Are you sure you want to log out?", parent=self)
        if (Exit > 0):
            self.destroy()
            self.window.show()
        else:
            if not Exit:
                return

    def slider(self):
        """creates slides for heading by taking the text,
        and that text are called after every 100 ms"""
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text + self.txt[self.count]
            self.heading.config(text=self.text)
        self.count += 1

        self.heading.after(100, self.slider)

    def heading_color(self):
        """
        configures heading label every 50 ms
        :return: new random color.

        """
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def time_running(self):
        """ displays the current date and time which is shown at top left corner of admin dashboard"""
        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%d/%m/%Y')
        concated_text = f"  {self.time} \n {self.date}"
        self.date_time.configure(text=concated_text, font=("times new roman", 13, "bold"), relief=FLAT
                                 , borderwidth=0, background="white", foreground="black")
        self.date_time.after(100, self.time_running)





if __name__ == '__main__':
    window = Tk()  # khoi tao cua so va gan root vao
    obj = Face_Recognition_System(window)
    window.mainloop()  # cua so hien len

