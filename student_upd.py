from datetime import datetime
import PIL
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import numpy as np
from tkinter import messagebox
from tkcalendar import DateEntry
from time import strftime
import cv2
import os
import re
import pymongo
from pymongo import MongoClient
from database_str import Database_str
from search_image import student_id
from search_image import StdImage
import base64
import threading
import shutil
import time
from io import BytesIO

mydata = []
class Student:

    def __init__(self,root):
        self.root=root
        w = 1350  # chiều dài giao diện
        h = 700  # chiều rộng giao diện

        ws = self.root.winfo_screenwidth()  # độ dài màn hình
        hs = self.root.winfo_screenheight()  # độ rộng màn
        x = (ws / 2) - (w / 2)  # vị trí cách lề trái x px
        y = (hs / 2) - (h / 2)  # vị trí cách lề trên y px

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # kích thước và vị trí hiển thị giao diện
        self.root.title("Student Management System")
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')
        today = strftime("%d-%m-%Y")

        # thông tin kết nối database
        self.db = Database_str()

        # ======================variables================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()  # khóa học
        self.var_semester = StringVar()  # cơ sở
        self.var_std_id = StringVar()  # id_hoc sinh
        self.var_std_name = StringVar()  # tên hoc sinh
        self.var_div = StringVar()  # lớp
        self.var_roll = StringVar()  # CMND
        self.var_gender = StringVar()  # giới tính
        self.var_dob = StringVar()  # ngày sinh
        self.var_email = StringVar()  # email
        self.var_phone = StringVar()  # SDT
        self.var_address = StringVar()  # Địa chỉ

        # ==================classvariables================
        self.var_class = StringVar()  # biến chứa lớp học
        self.var_nameclass = StringVar()  # biến tên lớp học
        # 取得課程資訊
        class_array = []  # 課程資訊陣列
        client = pymongo.MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        # 指定集合（collection）
        class_collection = db["class"]
        data = class_collection.find({}, {"_id": 0})
        insert_data = []  # 用來存放擷取到的資料
        for document in data:
            # 將每個文件的資料轉換成元組並添加到data中
            class_data = (
                document["Class"]


            )
            insert_data.append(class_data)

        print(insert_data)

        for i in insert_data:  # 對於每個在課程陣列中的課程：將該課程的信息傳遞到課程陣列中。
            class_array.append(i)

        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")  # Ảnh nền
        img3 = img3.resize((1350, 700), PIL.Image.ANTIALIAS)  # resize ảnh nền
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)  # label chứa ảnh nền
        bg_img.place(x=0, y=0, width=1350, height=700)

        # ==================================heading====================================
        # ====time====
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")  # Ảnh icon thời gian
        img_time = img_time.resize((27, 27), PIL.Image.ANTIALIAS)
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime, bg="white")
        time_img.place(x=43, y=40, width=27, height=27)

        def time():  # Hàm thời gian thay đổi mỗi giây
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(self.root, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl.place(x=80, y=35, width=100, height=18)
        time()  # chạy hàm time
        lbl1 = Label(self.root, text=today, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=18)

        # ====title=========
        self.txt = "Student Information Management"  # tiêu đề
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 22, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=400, y=22, width=650)
        # self.slider()
        # self.heading_color()

        main_frame = Frame(bg_img, bd=2, bg="white")  # main frame
        main_frame.place(x=24, y=90, width=1293, height=586)

        # left_label
        self.getNextid()  # chạy hàm nextid để lấy ra id tiếp theo trong bảng
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", font=("times new roman", 12, "bold"))
        Left_frame.place(x=7, y=10, width=655, height=565)

        label_Update_att = Label(Left_frame, bg="white", fg="red2", text="Student Information",
                                 font=("times new roman", 13, "bold"))
        label_Update_att.place(x=0, y=1, width=640, height=35)

        # Frame thông tin khóa học
        current_course_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Course Information",
                                          font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=35, width=640, height=100)

        # khóa học
        year_label = Label(current_course_frame, text="Course:", font=("times new roman", 11, "bold"), bg="white")
        year_label.grid(row=1, column=0, padx=15, sticky=W)

        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year,
                                  font=("times new roman", 11, "normal"), state="readonly",
                                  width=20)
        year_combo["values"] = ("Select a course", "2021", "2022", "2023")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=15, pady=10, sticky=W)

        # cơ sở(địa chỉ trường)
        semester_label = Label(current_course_frame, text="Base:", font=("times new roman", 11, "bold"), bg="white")
        semester_label.grid(row=1, column=2, padx=15, sticky=W)

        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester,
                                      font=("times new roman", 11, "normal"), state="readonly",
                                      width=20)
        semester_combo["values"] = ("Select campus", "JinDe", "BaoShan")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=15, pady=10, sticky=W)

        # frame thông tin lớp học
        class_student_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Class Information",
                                         font=("times new roman", 11, "bold"))
        class_student_frame.place(x=5, y=145, width=640, height=400)

        # Nhập Id học sinh
        studentID_label = Label(class_student_frame, text="Student ID:", font=("times new roman", 11, "bold"),
                                bg="white")
        studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.studentID_entry = Entry(class_student_frame, width=21, textvariable=self.var_std_id,
                                     font=("times new roman", 11, "normal"), state="disabled",
                                     )
        self.studentID_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Tên học sinh
        studentName_label = Label(class_student_frame, text="Student Name:", font=("times new roman", 11, "bold"),
                                  bg="white")
        studentName_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)

        studentName_entry = ttk.Entry(class_student_frame, width=23, textvariable=self.var_std_name,
                                      font=("times new roman", 11, "normal"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # Lớp học
        class_div_label = Label(class_student_frame, text="Subject:", font=("times new roman", 11, "bold"),
                                bg="white")
        class_div_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        class_div_entry = ttk.Combobox(class_student_frame, width=18, textvariable=self.var_div,
                                       font=("times new roman", 11, "normal"))
        class_div_entry["values"] = class_array
        class_div_entry.current()
        class_div_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # CMND
        roll_no_label = Label(class_student_frame, text="National ID:", font=("times new roman", 11, "bold"),
                              bg="white")
        roll_no_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        roll_no_entry = ttk.Entry(class_student_frame, width=23, textvariable=self.var_roll,
                                  font=("times new roman", 11, "normal"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # giới tính
        gender_label = Label(class_student_frame, text="Gender:", font=("times new roman", 11, "bold"),
                             bg="white")
        gender_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        # gender_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_gender ,font=("times new roman", 11, "bold"))
        # gender_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender,
                                    font=("times new roman", 11, "normal"), state="readonly",
                                    width=18)
        gender_combo["values"] = ("Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Ngày sinh
        dob_label = Label(class_student_frame, text="Birthday:", font=("times new roman", 11, "bold"),
                          bg="white")
        dob_label.grid(row=2, column=2, padx=10, pady=10, sticky=W)

        self.dob_entry = DateEntry(class_student_frame, width=18, bd=3, selectmode='day',
                                   year=2022, month=5, font=("times new roman", 12),
                                   day=22, date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=2, column=3, padx=10, pady=10, sticky=W)

        # email
        email_label = Label(class_student_frame, text="Email:", font=("times new roman", 11, "bold"),
                            bg="white")
        email_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        email_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_email,
                                font=("times new roman", 11, "normal"))
        email_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # SĐT
        phone_label = Label(class_student_frame, text="Phone number:", font=("times new roman", 11, "bold"),
                            bg="white")
        phone_label.grid(row=3, column=2, padx=10, pady=10, sticky=W)

        phone_entry = ttk.Entry(class_student_frame, width=23, textvariable=self.var_phone,
                                font=("times new roman", 11, "normal"))
        phone_entry.grid(row=3, column=3, padx=10, pady=10, sticky=W)

        # Địa chỉ
        address_label = Label(class_student_frame, text="Address:", font=("times new roman", 11, "bold"),
                              bg="white")
        address_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        address_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_address,
                                  font=("times new roman", 11, "normal"))
        address_entry.grid(row=4, column=1, padx=10, pady=10, sticky=W)

        # radioBtn
        self.var_radio1 = StringVar()
        radionbtn1 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="Has a photo", value="Yes")
        radionbtn1.grid(row=6, column=0)

        radionbtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="No photo", value="No")
        radionbtn2.grid(row=6, column=1)

        # ----------btn_frame----------------
        btn_frame = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=260, width=635, height=50)

        # nút lưu thông tin sinh viên
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")  # ảnh nút màu đỏ
        img_btn1 = img_btn1.resize((120, 35), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        save_btn = Button(btn_frame, text="Save", command=self.add_data, font=("times new roman", 11, "bold"), bd=0,
                          bg="white", cursor='hand2', activebackground='white',
                          width=115, image=self.photobtn1, fg="white", compound="center")
        save_btn.place(x=30, y=3)

        # nút sửa thông tin sinh viên
        update_btn = Button(btn_frame, text="Edit", command=self.update_data, font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=115, image=self.photobtn1, fg="white", compound="center")
        update_btn.place(x=180, y=3)

        # nút xóa thông tin sinh viên
        delete_btn = Button(btn_frame, text="Remove", command=self.delete_data, font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=115, image=self.photobtn1, fg="white", compound="center")
        delete_btn.place(x=330, y=3)

        # nút làm mới
        reset_btn = Button(btn_frame, text="Refresh", command=self.reset_data, font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=115, image=self.photobtn1, fg="white", compound="center")
        reset_btn.place(x=480, y=3)

        # ----------btn_frame1--------------
        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=320, width=635, height=50)

        # nút chụp ảnh học sinh
        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn2 = img_btn2.resize((170, 35), PIL.Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        take_photo_btn = Button(btn_frame1, text="Get student photo", command=self.generate_dataset,
                                font=("times new roman", 11, "bold"), bd=0, bg="white", cursor='hand2',
                                activebackground='white',
                                width=170, image=self.photobtn2, fg="white", compound="center")
        take_photo_btn.place(x=30, y=3)

        # nút train data từ các ảnh đã chụp
        update_photo_btn = Button(btn_frame1, text="Training Data", command=self.train_classifier,
                                  font=("times new roman", 11, "bold"), bd=0, bg="white", cursor='hand2',
                                  activebackground='white',
                                  width=170, image=self.photobtn2, fg="white", compound="center")
        update_photo_btn.place(x=230, y=3)

        # Nút xem các ảnh đã chụp của sinh viên
        show_photo_btn = Button(btn_frame1, text="View photo", command=self.student_image,
                                font=("times new roman", 11, "bold"), bd=0, bg="white", cursor='hand2',
                                activebackground='white',
                                width=170, image=self.photobtn2, fg="white", compound="center")
        show_photo_btn.place(x=430, y=3)

        # Frame bên phải chứa bảng dữ liệu và chức năng tìm kiếm
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=675, y=10, width=610, height=290)

        # Tìm kiếm
        search_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE, text="Search System",
                                  font=("times new roman", 11, "bold"))
        search_frame.place(x=5, y=5, width=600, height=70)

        self.var_com_search = StringVar()  # Loại tìm kiếm
        search_label = Label(search_frame, text="Search by:", font=("times new roman", 10, "bold"),
                             bg="white", fg="red2")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        search_combo = ttk.Combobox(search_frame, font=("times new roman", 10, "bold"), state="readonly",
                                    width=10, textvariable=self.var_com_search)
        search_combo["values"] = ("Student ID", "Student Name", "Course")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        #
        self.var_search = StringVar()  # Chữ cần tìm kiếm
        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman", 11, "bold"),
                                 textvariable=self.var_search)
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        # Nút tìm kiếm
        img_btn3 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")  # ảnh nền màu đỏ
        img_btn3 = img_btn3.resize((105, 35), PIL.Image.ANTIALIAS)  # resize ảnh
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)  # convert ảnh dạng ImageTk để truyền vào Button
        # nút tìm kiếm
        search_btn = Button(search_frame, text="Search", font=("times new roman", 11, "bold"), command=self.search_data,
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=105, image=self.photobtn3, fg="white", compound="center")
        search_btn.grid(row=0, column=3, padx=4)

        # nút xem tất cả
        showAll_btn = Button(search_frame, text="Show all", font=("times new roman", 11, "bold"),
                             command=self.fetch_data, bd=0, bg="white", cursor='hand2', activebackground='white',
                             width=105, image=self.photobtn3, fg="white", compound="center")
        showAll_btn.grid(row=0, column=4, padx=4)

        # Bảng dữ liệu
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=85, width=600, height=195)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        #不同的数据字段
        self.student_table = ttk.Treeview(table_frame, column=(
        "id", "year", "sem", "name", "div", "roll", "gender", "dob", "email", "phone", "address", "photo"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # đặt tên các cột dữ liệu
        self.student_table.heading("id", text="Student ID")
        # self.student_table.heading("dep",text="Chuyên ngành")
        # self.student_table.heading("course", text="Chương trình học")
        self.student_table.heading("name", text="Student name")
        self.student_table.heading("div", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Campus")
        self.student_table.heading("roll", text="National ID")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="Birthday")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone number")
        self.student_table.heading("address", text="Address")

        self.student_table.heading("photo", text="Image status")
        self.student_table["show"] = "headings"

        # độ dài các cột
        self.student_table.column("id", width=100)
        # self.student_table.column("dep", width=100)
        # self.student_table.column("course", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)

        self.student_table.column("div", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("photo", width=150)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)  # 按兩下列印到 txtbox 的資訊表時的事件
        self.fetch_data()  # load du lieu len bảng
        self.getNextid()  # Lấy id tiếp theo

        # ===============================bottomright-Class==============================
        # Thông tin lớp học và các chức năng thêm ,sửa ,xóa ,.....
        Underright_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                      font=("times new roman", 11, "bold"))
        Underright_frame.place(x=675, y=305, width=610, height=270)

        label_studentsb = Label(Underright_frame, bg="white", fg="red2", text="Classroom Management",
                                font=("times new roman", 12, "bold"))
        label_studentsb.place(x=0, y=1, width=600, height=35)

        # search
        self.var_com_searchclass = StringVar()  # Loại tìm kiếm lớp (theo lớp, tên lớp)
        search_combo = ttk.Combobox(Underright_frame, font=("times new roman", 11, "bold"),
                                    textvariable=self.var_com_searchclass,
                                    state="readonly",
                                    width=11)
        search_combo["values"] = ("Subject", "Course")
        search_combo.current(0)
        search_combo.grid(row=0, column=0, padx=10, pady=40, sticky=W)

        self.var_searchclass = StringVar()  # ký tự cần tìm
        searchstd_entry = ttk.Entry(Underright_frame, textvariable=self.var_searchclass, width=13,
                                    font=("times new roman", 10, "bold"))
        searchstd_entry.grid(row=0, column=1, padx=5, pady=35, sticky=W)

        # Các nút
        img_btn4 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")  # ảnh nút màu đỏ
        img_btn4 = img_btn4.resize((80, 25), PIL.Image.ANTIALIAS)
        self.photobtn4 = ImageTk.PhotoImage(img_btn4)

        # nút tìm kiếm
        searchstd_btn = Button(Underright_frame, command=self.search_Classdata, text="Search",
                               font=("times new roman", 10, "bold"), bd=0, bg="white", cursor='hand2',
                               activebackground='white',
                               width=80, image=self.photobtn4, fg="white", compound="center")
        searchstd_btn.grid(row=0, column=2, padx=3)

        # nút xem tất cả
        showAllstd_btn = Button(Underright_frame, text="View all", command=self.fetch_Classdata,
                                font=("times new roman", 10, "bold"), bd=0, bg="white", cursor='hand2',
                                activebackground='white',
                                width=80, image=self.photobtn4, fg="white", compound="center")
        showAllstd_btn.grid(row=0, column=3, padx=3)

        # Lớp học
        studentid_label = Label(Underright_frame, text="Subject:", font=("times new roman", 12, "bold"),
                                bg="white", width=12)
        studentid_label.place(x=20, y=100, width=100)

        studentid_entry = ttk.Entry(Underright_frame, textvariable=self.var_class,
                                    font=("times new roman", 12, "bold"), width=20)
        studentid_entry.place(x=135, y=100, width=200)

        # Tên lớp học
        subsub_label = Label(Underright_frame, text="Course:", font=("times new roman", 12, "bold"),
                             bg="white")
        subsub_label.place(x=30, y=145, width=80)

        subsub_entry = ttk.Entry(Underright_frame, width=22, textvariable=self.var_nameclass,
                                 font=("times new roman", 12, "bold"))
        subsub_entry.place(x=135, y=145, width=200)

        # btn_frame
        btn_framestd = Frame(Underright_frame, bg="white", bd=2, relief=RIDGE)
        btn_framestd.place(x=10, y=200, width=400, height=55)

        img_btn5 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn5 = img_btn5.resize((90, 30), PIL.Image.ANTIALIAS)
        self.photobtn5 = ImageTk.PhotoImage(img_btn5)

        # nút thêm lớp học
        addTc_btn = Button(btn_framestd, text="Add", command=self.add_Classdata,
                           font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=90, image=self.photobtn5, fg="white", compound="center"
                           )
        addTc_btn.place(x=5, y=7)

        # nút xóa lớp học
        deleteTc_btn = Button(btn_framestd, text="Remove", command=self.delete_Classdata,
                              font=("times new roman", 11, "bold"),
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=90, image=self.photobtn5, fg="white", compound="center"
                              )
        deleteTc_btn.place(x=103, y=7)

        # nút cập nhật thông tin lớp học
        updateTc_btn = Button(btn_framestd, text="Modify", command=self.update_Classdata,
                              font=("times new roman", 11, "bold"),
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=90, image=self.photobtn5, fg="white", compound="center")
        updateTc_btn.place(x=201, y=7)

        # nút làm mới
        resetTc_btn = Button(btn_framestd, text="Refresh", command=self.reset_Classdata,
                             font=("times new roman", 11, "bold"),
                             bd=0, bg="white", cursor='hand2', activebackground='white',
                             width=90, image=self.photobtn5, fg="white", compound="center")
        resetTc_btn.place(x=299, y=7)

        # bảng dữ liệu lớp học
        tablestd_frame = Frame(Underright_frame, bd=2, relief=RIDGE, bg="white")
        tablestd_frame.place(x=420, y=35, width=180, height=220)

        # scroll bar
        scroll_x = ttk.Scrollbar(tablestd_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablestd_frame, orient=VERTICAL)

        self.StudentTable = ttk.Treeview(tablestd_frame, column=(
            "Subject", "Class"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.StudentTable.xview)
        scroll_y.config(command=self.StudentTable.yview)

        self.StudentTable.heading("Subject", text="Subject")
        self.StudentTable.heading("Class", text="Course")

        self.StudentTable["show"] = "headings"
        self.StudentTable.column("Subject", width=80)
        self.StudentTable.column("Class", width=80)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease>", self.get_cursorClass)
        self.fetch_Classdata()

    # ============function declaration===============
    def student_image(self):  # Xem ảnh của học sinh
        if self.var_std_name.get() == "" or self.var_std_id.get() == "":  #学生的姓名或学生的ID为空，则报错
            messagebox.showerror("Error", "Please enter complete information", parent=self.root)
        else:
            student_id(self.var_std_id.get())  # 将学生的ID传递到图像信息表单
            self.new_window = Toplevel(self.root)  #新窗口
            self.app = StdImage(self.new_window)  # 显示图像查看界面

    def getNextid(self):  # 取下一个ID
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        student_collection = db["student"]
        last_id_result = student_collection.find_one(
            {},
            {"Student ID": 1},
            sort=[("Student ID", pymongo.DESCENDING)]
        )
        lastid = last_id_result["Student ID"]
        if (lastid == None):
            self.var_std_id.set("1")  # Nếu ko có dữ liệu -> id tiếp theo=1
        else:  # Nếu có id tiếp theo bằng id cũ +1
            nextid = int(lastid) + 1
            self.var_std_id.set(str(nextid))


    def add_data(self):  # Thêm dữ liệu
        # ========check class================
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # để Check xem email nhập vào có đúng định dạng email ko

        # 查询 MongoDB 以获取所有的 Class
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        class_collection = db["class"]
        class_result = class_collection.find({}, {"Class": 1, "_id": 0})

        insert_data = []  # 用來存放擷取到的資料
        for document in class_result:
            # 將每個文件的資料轉換成元組並添加到data中
            class_data = (
                document["Class"]

            )
            insert_data.append(class_data)

        print(insert_data)

        # 提取 Class 的值，如果文档存在

        arrayClass = []
        for chc in insert_data:
            # print(chc[0])
            arrayClass.append(chc)
        print(arrayClass)
        if self.var_std_name.get() == "" or self.var_std_id.get() == "" or self.var_div.get() == "":
            messagebox.showerror("Error", "Please enter complete information", parent=self.root)
        elif (self.var_div.get() not in arrayClass):  # Lớp ko tồn tại thì thông báo
            messagebox.showerror("Error", "Classroom name does not exist! Please check again", parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):  # check email nhập vào đúng định dạng
            messagebox.showerror("Error", "Please enter email in the correct format", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):  # SDT nhạp vào đúng dạng số ko
            messagebox.showerror("Error", "Please enter the correct phone number", parent=self.root)
        elif (self.var_roll.get().isalnum() != True):  # CMND đúng dạng số ko
            messagebox.showerror("Error", "Please enter the correct ID number", parent=self.root)
        else:  # Thêm thông tin học sinh
            try:
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                # 指定集合（collection）
                collection = db["student"]

                year = int(self.var_year.get())
                semester = str(self.var_semester.get())
                name = str(self.var_std_name.get())
                div = str(self.var_div.get())
                nid = str(self.var_roll.get())
                gender = str(self.var_gender.get())
                bday = str(self.dob_entry.get_date().strftime('%Y-%m-%d'))
                email = str(self.var_email.get())
                phone = str(self.var_phone.get())
                address = str(self.var_address.get())
                image_status = str(self.var_radio1.get())
                student_id = int(self.var_std_id.get())




                data_to_insert = {
                    "Student ID": student_id,
                    "Year": year,
                    "Campus": semester,
                    "Student name": name,
                    "Course": div,
                    "National ID": nid,
                    "Gender": gender,
                    "Birthday": bday,
                    "E-mail": email,
                    "Phone number": phone,
                    "Address": address,
                    "Image status": image_status
                }
                result = collection.insert_one(data_to_insert)
                print(f"Inserted document id: {result.inserted_id}")


                self.fetch_data()  # In dữ liệu mới lên bảng sau khi thêm
                self.reset_data()  # reset lại các txtbox để nhập dữ liệu mới

                messagebox.showinfo("Success", "Added student information successfully",
                                    parent=self.root)  # thêm thành công
            except Exception as es:  # Nếu có lỗi -> in ra màn hình
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    # =======================fetch-data========================
    def fetch_data(self):#取得所有學生資訊
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        student_collection = db['student']

        data = []  # 用來存放擷取到的資料

        # 使用find方法從集合中擷取所有資料
        cursor = student_collection.find()

        for document in cursor:
            # 將每個文件的資料轉換成元組並添加到data中
            student_data = (
                document["Student ID"],
                document["Year"],
                document["Campus"],
                document["Student name"],
                document["Course"],
                document["National ID"],
                document["Gender"],
                document["Birthday"],
                document["E-mail"],
                document["Phone number"],
                document["Address"],
                document["Image status"]
            )
            data.append(student_data)

            # 顯示資料到表格上，這部分與原始程式碼相同
            if len(data) > -1:
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END, values=i)

            client.close()  # 關閉與MongoDB的連接

    # ======================get-cursor==============================
    def get_cursor(self,event=""):#點擊表格時，將詳細資訊顯示在各個文字框中。
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        dob_string = data[7]  # Assuming data[7] contains the date string like '2002-02-08'
        dob_date = datetime.strptime(dob_string, '%Y-%m-%d').date()#將一個符合特定格式的日期字串（例如"2023-09-18"）轉換成對應的日期物件。
        self.var_std_id.set(data[0]),
        self.var_year.set(data[1]),
        self.var_semester.set(data[2]),
        self.var_std_name.set(data[3]),
        self.var_div.set(data[4]),
        self.var_roll.set(data[5]),
        self.var_gender.set(data[6]),
        self.dob_entry.set_date(dob_date),
        self.var_email.set(data[8]),
        self.var_phone.set(data[9]),
        self.var_address.set(data[10]),
        self.var_radio1.set(data[11]),


    def update_data(self):#Cập nhật thông tin học sinh
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
        if  self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Please enter complete information",parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):
            messagebox.showerror("Error", "Please enter email in the correct format", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):
            messagebox.showerror("Error", "Please enter the correct phone number", parent=self.root)
        elif (self.var_roll.get().isalnum() != True):
            messagebox.showerror("Error", "Please enter the correct ID number", parent=self.root)
        else:
            try:
            	#Hỏi trước khi cập nhật
                Update=messagebox.askyesno("Update","Do you want to update this student's information?",parent=self.root)
                if Update>0:#nếu bấm yes
                    # 建立MongoDB連線
                    client = pymongo.MongoClient(
                        "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                    # 指定資料庫
                    db = client["Face_Recognizer"]
                    # 指定集合（collection）
                    collection = db["student"]

                    year = int(self.var_year.get())
                    semester = str(self.var_semester.get())
                    name = str(self.var_std_name.get())
                    div = str(self.var_div.get())
                    nid = str(self.var_roll.get())
                    gender = str(self.var_gender.get())
                    bday = str(self.dob_entry.get_date().strftime('%Y-%m-%d'))
                    email = str(self.var_email.get())
                    phone = str(self.var_phone.get())
                    address = str(self.var_address.get())
                    image_status = str(self.var_radio1.get())
                    student_id = int(self.var_std_id.get())

                    query = {"Student ID": student_id}

                    data_to_update = {
                        '$set': {
                            "Year": year,
                            "Campus": semester,
                            "Student name": name,
                            "Course": div,
                            "National ID": nid,
                            "Gender": gender,
                            "Birthday": bday,
                            "E-mail": email,
                            "Phone number": phone,
                            "Address": address,
                            "Image status": image_status
                        }
                    }

                    result = collection.update_one(query, data_to_update)

                    # 檢查更新結果
                    if result.matched_count > 0:
                        print("文檔匹配成功")

                        if result.modified_count > 0:
                            print("文檔成功更新")
                        else:
                            print("文檔未被更新（可能已經包含相同的數據）")
                    else:
                        print("沒有匹配到任何文檔")

                else:
                    if not Update:#按下返回
                        return
                messagebox.showinfo("Success","Update student information successfully",parent=self.root)
                self.fetch_data()#Hiện thị dữ liệu sau update
                self.reset_data()#Lám mới các txtbox
            except Exception as es:
                messagebox.showerror("Eror",f"Due To:{str(es)}",parent=self.root)

    #Delete Function
    def delete_data(self):#Xóa thông tin học sinh theo mã id
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","Student ID cannot be left blank",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Delete student","Do you want to delete this student?",parent=self.root)
                if delete>0:

                        val=(self.var_std_id.get(),)

                        name = self.var_std_name.get()
                        id = self.var_std_id.get()
                        folder_name = name + "_" + id
                        try:
                            shutil.rmtree(folder_name)
                            print(f'Folder {folder_name} deleted successfully!')
                        except OSError as e:
                            print(f'Error: {folder_name} deleted failed. - {e}')

                        # 建立MongoDB連線
                        client = pymongo.MongoClient(
                                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                        # 指定資料庫
                        db = client["student_photo"]
                        # 指定集合（collection）
                        collection = db[f"{name}"]

                        # 删除数据库
                        collection.drop()

                        print(f'集合 {collection} 已成功删除')

                        # 指定資料庫
                        db = client["Face_Recognizer"]
                        # 指定集合（collection）
                        student_collection = db["student"]
                        # 使用delete_one方法刪除符合條件的一筆資料
                        result = student_collection.delete_one({"Student ID": int(id)})

                        # 檢查刪除是否成功
                        if result.deleted_count == 1:
                            print(f"Successfully deleted student with student_id: {id}")
                        else:
                            print(f"Student with student_id: {id} not found")


                else:
                    if not delete:
                        return
                self.reset_data()
                self.fetch_data()
                messagebox.showinfo("Delete","Delete student successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # ===================Reset function====================
    def reset_data(self):#Reset function txtbox information
        # self.var_dep.set("Chọn chuyên ngành"),
        # self.var_course.set("Chọn hệ"),
        self.var_year.set("Select a course"),
        self.var_semester.set("Select a branch"),
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_div.set(""),
        self.var_roll.set(""),
        self.var_gender.set("Male"),
        self.dob_entry.set_date(strftime("%d/%m/%Y")),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),

        self.var_radio1.set(""),
        self.getNextid()
    def search_data(self):#Hàm tìm kiếm
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
            if self.var_com_search.get() == "" or self.var_search.get() == "":
                messagebox.showerror("Error!", "Please enter complete information.",parent=self.root)

            else:
                try:
                    # global mydata
                    client = pymongo.MongoClient(
                        "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                    # 指定資料庫
                    db = client["Face_Recognizer"]
                    # 指定集合（collection）
                    student_collection = db["student"]

                    #convert loại tìm kiếm về tên các côt trọng mysql
                    if (self.var_com_search.get() == "Student ID"):
                        self.var_com_search.set("Student_id")
                    elif (self.var_com_search.get() == "Student name"):
                        self.var_com_search.set("Name")
                    elif (self.var_com_search.get() == "Administrative class"):
                        self.var_com_search.set("Class")
                    #câu lệnh tìm kiếm
                    search_condition = {str(self.var_com_search.get()): {"$regex": str(self.var_com_search.get())}}
                    data = student_collection.find(search_condition, {"_id": 0})
                    insert_data = []  # 用來存放擷取到的資料
                    for document in data:
                        # 將每個文件的資料轉換成元組並添加到data中
                        class_data = (
                            document["IdAuttendance"],
                            document["Student_id"],
                            document["Name"],
                            document["class"],
                            document["Time_in"],
                            document["Time_out"],
                            document["Date"],
                            document["Lesson_id"],
                            document["AttendanceStatus"],

                        )
                        insert_data.append(class_data)

                    print(insert_data)

                    if (len(insert_data) > -1):#Nếu có dữ liệu thì in lên bảng
                        self.student_table.delete(*self.student_table.get_children())
                        for i in insert_data:
                            self.student_table.insert("", END, values=i)
                        #thông báo có bao nhiêu dữ liệu tìm kiếm đc
                        messagebox.showinfo("Notification", "Yes " + str(len(data)) + " Records that satisfy the condition",parent=self.root)

                    else:#nếu ko có dữ liệu thông báo ko có bản ghi
                        self.student_table.delete(*self.student_table.get_children())
                        messagebox.showinfo("Notification", " No records match the condition",parent=self.root)
                    client.close()
                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
    #=============generate dataset and take photo=================
    def generate_dataset(self):#Chụp ảnh học sinh
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
        if  self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Please enter full information",parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):
            messagebox.showerror("Error", "Please enter a valid email address", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):
            messagebox.showerror("Error", "Please enter a valid phone number", parent=self.root)
        elif (self.var_roll.get().isalnum() != True):
            messagebox.showerror("Error", "Please enter a valid ID number", parent=self.root)
        else:
            try:#update thông tin học sinh
                # global mydata
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                # 指定集合（collection）
                student_collection = db["student"]

                # 定義搜索條件，這裡假設你的搜索條件是 "Student_id" 等於 self.var_std_id.get()
                search_condition = {"Student_id": self.var_std_id.get()}

                # 定義更新的數據
                update_data = {
                    "$set": {
                        "Year": self.var_year.get(),
                        "Semester": self.var_semester.get(),
                        "Name": self.var_std_name.get(),
                        "Class": self.var_div.get(),
                        "Roll": self.var_roll.get(),
                        "Gender": self.var_gender.get(),
                        "Dob": self.dob_entry.get_date().strftime('%Y-%m-%d'),
                        "Email": self.var_email.get(),
                        "Phone": self.var_phone.get(),
                        "Address": self.var_address.get(),
                        "PhotoSample": self.var_radio1.get(),
                    }
                }
                # 執行更新操作
                student_collection.update_one(search_condition, update_data)

                # 關閉 MongoDB 連接
                client.close()


                # my_cursor.execute("select * from student")
                # myresult=my_cursor.fetchall()
                id=self.var_std_id.get()
                name = self.var_std_name.get()
                mongo_str = id + "_" + name
                # for x in myresult:
                #     id+=1

                self.reset_data()
                self.fetch_data()


                # =========load haar===================
                face_classifier = cv2.CascadeClassifier(
                    "haarcascade_frontalface_default.xml")  # Model phát hiện khuôn mặt trong màn hình
                # 建立MongoDB連線
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["student_photo"]
                # 指定集合（collection）
                collection = db[f"{mongo_str}"]
                def face_cropped(img):  # Cắt khuôn mặt đã phát hiện theo hình ô vuông
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # chuyển ảnh về dạng gray để phát hiện khuôn mặt
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)  # tỉ lệ của thuật toán phát hiện khuôn mặt
                    # scaling factor 1.3
                    ##minimum neighbor 5
                    for (x, y, w, h) in faces:  # với mỗi khuôn mặt phát hiện trên khung hình, cắt khuôn mặt ra
                        face_cropped = img[y:y + h, x:x + w]
                        return face_cropped

                cap = cv2.VideoCapture(0)  # Mở camera webcam(=0) bằng thư viện xử lý ảnh opencv
                img_id = 0  # Số ảnh chụp
                folder_name = "student_photo"
                print(folder_name)

                # 記錄開始時間
                start_time = time.time()

                while True:  # Nếu ko có lỗi mở cam
                    net, my_frame = cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id += 1  # với mỗi ảnh chụp đc tăng số ảnh lên 1
                        # face=cv2.resize(face_cropped(my_frame),(190,190))
                        face = cv2.cvtColor(face_cropped(my_frame), cv2.COLOR_BGR2GRAY)

                        # 创建新文件夹，如果它不存在
                        if not os.path.exists("student_photo"):
                            os.makedirs("student_photo")
                            print(f"Folder {folder_name} established")

                        file_name = os.path.join(folder_name, f"{id}_face_{img_id}.jpg")
                        try:
                            retval, img_buffer = cv2.imencode('.jpg', face)
                            if retval:
                                with open(file_name, 'wb') as file:
                                    file.write(img_buffer)
                                print(f"Save file successfully：{file_name}")
                            else:
                                print(f"Save file failed.")
                        except Exception as e:
                            print(f"Exception while saving file：{e}")

                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),
                                    2)  # 在 face 圖像上添加一個指定文本，該文本包括圖像的 ID（轉換為字符串形式）
                        cv2.imshow("Cropped Face", face)  # 使用 OpenCV 的 imshow 函數來顯示圖像窗口

                    if cv2.waitKey(1) == 13 or int(img_id) == 100:  # 達成條件時終止拍攝
                        break
                cap.release()  # 使用 release() 方法釋放先前創建的 VideoCapture 對象
                cv2.destroyAllWindows()  # 關閉所有已經通過 cv2.imshow() 打開的窗口，使它們都被銷毀。
                #messagebox.showinfo("Complete", "Done!", parent=self.root)




                def close_self(self):
                    self.destroy()

                # 循环结束后一次性上传到 MongoDB
                def upload_to_mongodb(file_path, img_id, collection):

                    with open(file_path, 'rb') as file:
                        img_buffer = file.read()

                    base64_img = base64.b64encode(img_buffer).decode('utf-8')
                    data = {
                        "photo_id": img_id,
                        "image": base64_img
                    }
                    collection.insert_one(data)


                def upload_images_to_mongodb(folder_name, collection, target_student_id):

                    try:
                        for root, dirs, files in os.walk(folder_name):
                            threads = []
                            img_id = 0

                            for file in files:
                                file_path = os.path.join(root, file)

                                # 檢查檔案名是否包含指定的學生ID
                                if f"{target_student_id}_face_" in file:
                                    img_id += 1

                                    # 創建一個線程來上傳到 MongoDB
                                    thread = threading.Thread(target=upload_to_mongodb,
                                                              args=(file_path, img_id, collection))
                                    thread.start()
                                    threads.append(thread)

                            # 等待所有線程完成
                            for thread in threads:
                                thread.join()

                        end_time = time.time()

                        # 計算代碼執行時間
                        execution_time = end_time - start_time

                        print(f"代碼執行時間: {execution_time} 秒")
                        messagebox.showinfo("Upload Complete", "Images uploaded successfully.")

                    except Exception as e:
                        messagebox.showerror("Error", f"Error during upload: {str(e)}")



                upload_images_to_mongodb(folder_name, collection, id)

            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)  # 例外處理


    # ==========================TrainDataSet=======================

    def train_classifier(self):  # Hàm train model nhận diện
        # 記錄開始時間
        start_time = time.time()

        # 連接到MongoDB
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["student_photo"]

        # 從MongoDB檢索數據
        faces = []
        ids = []

        for collection_name in db.list_collection_names():

            id = collection_name.split('_')[0]
            print(id)
            # 在集合中遍歷每個學生文檔
            collection = db[collection_name]
            for student in collection.find():
                base64_image = student.get("image", "")
                if base64_image:
                    # 將base64字符串轉換為numpy數組
                    image_data = BytesIO(base64.b64decode(base64_image))
                    img = PIL.Image.open(image_data).convert('L')
                    image_np = np.array(img, 'uint8')

                    faces.append(image_np)
                    ids.append(int(id))

                    cv2.imshow("Training", image_np)
                    cv2.waitKey(1) == 13

        ids = np.array(ids)

        # =================訓練數據分類器並保存============

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")

        cv2.destroyAllWindows()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"模型訓練時間: {execution_time} 秒")
        messagebox.showinfo("Outcome", "Training dataset Completed", parent=self.root)

    # ========================================Function Student======================================

    def get_cursorClass(self, event=""):  # sự kiện ckick vào bảng lớp học
        cursor_row = self.StudentTable.focus()
        content = self.StudentTable.item(cursor_row)
        rows = content['values']
        self.var_class.set(rows[0])
        self.var_nameclass.set(rows[1])

    def add_Classdata(self):  # Thêm lớp học
        client = pymongo.MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["student_photo"]
        # 指定集合（collection）
        class_collection = db["class"]
        ckClass = class_collection.find({},{"_id": 0})
        ckClass = list(ckClass)

        arrayClass = []
        for chs in ckClass:
            # print(chs[0])
            arrayClass.append(str(chs[0]))

        if self.var_class.get() == "" or self.var_nameclass.get() == "":
            messagebox.showerror("Error", "Please enter complete information!", parent=self.root)

        elif (self.var_class.get() in arrayClass):  # 檢查輸入的班級是否已存在
            messagebox.showerror("Error", "Class already exist! Please check again!", parent=self.root)
        else:
            try:
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["student_photo"]
                # 指定集合（collection）
                class_collection = db["class"]

                class_data = {
                    "Class": self.var_class.get(),
                    "NameClass": self.var_nameclass.get(),
                }

                class_collection.insert_one(class_data)


                self.fetch_Classdata()
                self.reset_Classdata()

                messagebox.showinfo("Success", "Successfully added class information!",
                                        parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def reset_Classdata(self):  # làm mới
        self.var_class.set("")
        self.var_nameclass.set("")

    def fetch_Classdata(self):  # Hiện thị các lớp học
        # global mydata
        # mydata.clear()
        client = pymongo.MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        # 指定集合（collection）
        class_collection = db["class"]
        data = class_collection.find({}, {"_id": 0})
        insert_data = []  # 用來存放擷取到的資料
        for document in data:
            # 將每個文件的資料轉換成元組並添加到data中
            class_data = (
                document["Class"],
                document["Name"],

            )
            insert_data.append(class_data)

        print(insert_data)

        if len(insert_data) != 0:  # nếu có dữ liệu thì in lên bảng
            self.StudentTable.delete(*self.StudentTable.get_children())
            for i in insert_data:
                self.StudentTable.insert("", END, values=i)

        client.close()

    def update_Classdata(self):  # Cập nhật thông tin lớp học
            if self.var_class == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Please enter complete information.", parent=self.root)

            else:
                try:
                    Update = messagebox.askyesno("Update", "Do you want to update this record?", parent=self.root)
                    if Update > 0:
                        client = pymongo.MongoClient(
                            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                        # 指定資料庫
                        db = client["Face_Recognizer"]
                        # 指定集合（collection）
                        class_collection = db["class"]
                        print(self.var_nameclass.get())
                        print(self.var_class.get())
                        class_collection.update_one(
                            {"Class": str(self.var_class.get())},
                            {"$set": {"Name": str(self.var_nameclass.get())}}

                        )

                        client.close()
                    else:
                        if not Update:
                            return
                    messagebox.showinfo("Success", "Successfully updated class information.",
                                        parent=self.root)

                    self.reset_Classdata()
                    self.fetch_Classdata()

                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

            # Delete Function

    def delete_Classdata(self):  # Xóa lớp học
            if self.var_class == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Do not leave information blank! ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Delete record", "Do you want to delete this record?", parent=self.root)
                    if delete > 0:
                        client = pymongo.MongoClient(
                            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                        # 指定資料庫
                        db = client["Face_Recognizer"]
                        # 指定集合（collection）
                        class_collection = db["class"]
                        # 在 MongoDB 中删除数据
                        class_collection.delete_one({"Class": self.var_class.get()})

                        # 关闭 MongoDB 连接
                        client.close()

                    else:
                        if not delete:
                            return

                    # self.fetch_data()
                    messagebox.showinfo("Delete", "Record deleted successfully.", parent=self.root)
                    self.reset_Classdata()
                    self.fetch_Classdata()
                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def search_Classdata(self):  #Find class information.
            if self.var_com_searchclass.get() == "" or self.var_searchclass.get() == "":
                messagebox.showerror("Error", "Please input complete information!", parent=self.root)

            else:
                try:
                    client = pymongo.MongoClient(
                        "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                    # 指定資料庫
                    db = client["Face_Recognizer"]
                    # 指定集合（collection）
                    class_collection = db["class"]
                    # 在 MongoDB 中执行查询


                    if (self.var_com_searchclass.get() == "Subject"):
                        self.var_com_searchclass.set("Class")
                    elif (self.var_com_searchclass.get() == "Course"):
                        self.var_com_searchclass.set("Name")

                    query = {str(self.var_com_searchclass.get()): {"$regex": f".*{str(self.var_searchclass.get())}.*"}}
                    data = class_collection.find(query, {"_id": 0})
                    insert_data = []  # 用來存放擷取到的資料
                    for document in data:
                        # 將每個文件的資料轉換成元組並添加到data中
                        class_data = (
                            document["Class"],
                            document["Name"],

                        )
                        insert_data.append(class_data)

                    if len(insert_data) != 0:
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        for i in insert_data:
                            self.StudentTable.insert("", END, values=i)
                        messagebox.showinfo("Notification", "We have " + str(len(insert_data)) + " record(s) match the condition.",
                                            parent=self.root)

                    else:
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        messagebox.showinfo("Notification", "No records match the condition.", parent=self.root)

                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()  # khoi tao cua so va gan root vao

    obj = Student(root)
    root.mainloop()  # cua so hien len





