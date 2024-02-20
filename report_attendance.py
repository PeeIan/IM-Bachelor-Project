import csv

from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
from time import strftime
import calendar
import time
from tkinter import messagebox
import mysql.connector
import pandas as pd
from tkcalendar import DateEntry
from database_str import Database_str
import pymongo
from pymongo import MongoClient

mydata=[]#mảng dữ liệu cho điểm danh muộn
mydataNot=[]#mảng dữ liệu điểm danh vắng
mydataNotInAtt=[]#mảng dữ liệu học sinh ko điểm danh
class Report:
    def __init__(self,root):
        self.root=root
        w = 1350  # chiều dài giao diện
        h = 700  # chiều rộng giao diện

        ws = self.root.winfo_screenwidth()  # độ dài màn hình
        hs = self.root.winfo_screenheight()  # độ rộng màn
        x = (ws / 2) - (w / 2)  # vị trí cách lề trái x px
        y = (hs / 2) - (h / 2)  # vị trí cách lề trên y px
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # icon của giao diện
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # kích thước và vị trí hiển thị giao diện
        self.root.title("Facial Recognition System")
        self.today = strftime("%d-%m-%Y")#thời gian ngày-tháng-năm hiện tại
        self.today_time = strftime("%d/%m/%Y")

        # thông tin kết nối database
        self.db = Database_str()
        
        #===========variable============
        self.student = StringVar()#biến student để đếm số học sinh trong database sau khi truy vấn
        self.att=StringVar()#số bản điểm danh
        self.late=StringVar()#số lần đi muộn của các học sinh
        self.noatt=StringVar()# số lần vắng của các học sinh

        img3 = PIL.Image.open(r"ImageFaceDetect\bg1.png")#mở ảnh nền
        img3 = img3.resize((1350, 700), PIL.Image.ANTIALIAS)#resize kích thước ảnh
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1350, height=700)

        # ==================================heading====================================
        # =========time=========

        # ========title=========
        self.txt = "System Statistics"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 18, "bold"), bg="white", fg="black",
                             bd=0, relief=FLAT)
        self.heading.place(x=350, y=20, width=600)
        # self.slider()
        # self.heading_color()

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=23, y=75, width=1300, height=600)

        # ===================Top_label=====================
        Top_frame=LabelFrame(main_frame, bd=0, bg="white",
                                font=("times new roman", 12, "bold"))
        Top_frame.place(x=5,y=0,width=1280,height=120)
        #===================select_for_txt=================
        client = pymongo.MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        # 指定集合（collection）
        student_collection = db["student"]
        #========student==========
        # Count the number of documents in the student collection in MongoDB
        count_st = student_collection.count_documents({})
        self.student.set(str(count_st))

        #=======attendance========
        attendance_collection = db["attendance"]
        # Count the number of documents in the attendance collection in MongoDB
        count_att = attendance_collection.count_documents({})
        self.att.set(str(count_att))
        #=======đi muộn=============
        count_late = attendance_collection.count_documents({"AttendanceStatus": {"$regex": "Late"}})
        self.late.set(str(count_late))
        #========không điểm danh=======
        #not_in_attendance_table
        pipeline = [
            {
                "$lookup": {
                    "from": "class",
                    "localField": "Class",
                    "foreignField": "Class",
                    "as": "class_info"
                }
            },
            {
                "$lookup": {
                    "from": "lesson",
                    "localField": "Lesson_id",
                    "foreignField": "Lesson_id",
                    "as": "lesson_info"
                }
            },
            {
                "$lookup": {
                    "from": "attendance",
                    "let": {
                        "student_id": "$Student ID",
                        "lesson_id": "$Lesson_id"
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": [
                                        "$Student_id",
                                        "$$student_id"
                                    ],
                                    "$eq": [
                                        "$Lesson_id",
                                        "$$lesson_id"
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "attendance_info"
                }
            },
            {
                "$match": {
                    "attendance_info": {
                        "$size": 0
                    },
                    "lesson_info.Date": {
                        "$lte": self.today_time
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
        lesson_collection = db["lesson"]

        result = list(lesson_collection.aggregate(pipeline))

        count_noatt = result[0]["count"] if result else 0


        #có điểm danh nhưng điểm danh quá muộn giờ học
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {"AttendanceStatus": {"$regex": "Absent"}}
                    ]
                }
            },
            {
                "$group": {
                    "_id": None,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]

        result = list(attendance_collection.aggregate(pipeline))
        count_noatt1 = result[0]["count"] if result else 0

        a = int(count_noatt) + int(count_noatt1)
        self.noatt.set(a)

        #student_frame
        student_frame=LabelFrame(Top_frame,bd=1,bg='#27a9e3')
        student_frame.place(x=5,y=0,width=315,height=110)

        img_student = PIL.Image.open(r"ImageFaceDetect\sv.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgsv = ImageTk.PhotoImage(img_student)
        student_img = Label(student_frame, image=self.photoimgsv, bg="#27a9e3")
        student_img.place(x=20, y=40, width=50, height=50)
        student_text=Label(student_frame,text="Students number",font=("times new roman", 18, "bold"),fg="white",bg="#27a9e3")
        student_text.place(x=100,y=30)
        student_text = Label(student_frame,textvariable=self.student, font=("times new roman", 15, "bold"),fg="white",bg="#27a9e3")
        student_text.place(x=100, y=70)

        #attendance_success
        att_frame = LabelFrame(Top_frame, bd=1, bg='#28b779')
        att_frame.place(x=335, y=0, width=315, height=110)

        img_att = PIL.Image.open(r"ImageFaceDetect\sodd.png")
        img_att = img_att.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgatt = ImageTk.PhotoImage(img_att)
        att_img = Label(att_frame, image=self.photoimgatt, bg="#28b779")
        att_img.place(x=20, y=40, width=50, height=50)
        att_text = Label(att_frame, text="Attendant number", font=("times new roman", 18, "bold"), fg="white",
                             bg="#28b779")
        att_text.place(x=100, y=30)
        att_text = Label(att_frame, textvariable=self.att, font=("times new roman", 15, "bold"), fg="white",
                             bg="#28b779")
        att_text.place(x=100, y=70)

        #late_attendance
        late_frame = LabelFrame(Top_frame, bd=1, bg='#852b99')
        late_frame.place(x=665, y=0, width=315, height=110)

        img_late = PIL.Image.open(r"ImageFaceDetect\late.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimglate = ImageTk.PhotoImage(img_late)
        late_img = Label(late_frame, image=self.photoimglate, bg="#852b99")
        late_img.place(x=20, y=40, width=50, height=50)
        late_text = Label(late_frame, text="Late number", font=("times new roman", 18, "bold"), fg="white",
                         bg="#852b99")
        late_text.place(x=100, y=30)
        late_text = Label(late_frame, textvariable=self.late, font=("times new roman", 15, "bold"), fg="white",
                         bg="#852b99")
        late_text.place(x=100, y=70)

        #no_attendance
        late_frame = LabelFrame(Top_frame, bd=1, bg='#DC143C')
        late_frame.place(x=990, y=0, width=315, height=110)

        img_noatt = PIL.Image.open(r"ImageFaceDetect\vang.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgnoatt = ImageTk.PhotoImage(img_noatt)
        noatt_img = Label(late_frame, image=self.photoimgnoatt, bg="#DC143C")
        noatt_img.place(x=20, y=40, width=50, height=50)
        noatt_text = Label(late_frame, text="Absent number", font=("times new roman", 18, "bold"), fg="white",
                          bg="#DC143C")
        noatt_text.place(x=100, y=30)
        noatt_text = Label(late_frame, textvariable=self.noatt, font=("times new roman", 15, "bold"), fg="white",
                          bg="#DC143C")
        noatt_text.place(x=100, y=70)

        #====================Left_label====================
        Left_frame = LabelFrame(main_frame, bd=2, bg="white",
                               font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=125, width=645, height=470)
        #danh sách hs đi muộn
        self.late_group=LabelFrame(Left_frame,bd=1,bg="white",text="Late students",font=("times new roman", 11, "bold"),fg="black",relief=RIDGE)
        self.late_group.place(x=0,y=0,width=630,height=220)

        self.var_com_searchlate = StringVar()#biến chọn loại tìm kiếm
        search_combo = ttk.Combobox(self.late_group, font=("times new roman", 11, "bold"),
                                    textvariable=self.var_com_searchlate,
                                    state="read only",
                                    width=11)
        search_combo["values"] = ("Student ID", "Date","Lesson ID","Class")
        search_combo.current(0)
        search_combo.bind("<<ComboboxSelected>>", self.callbackLate)
        search_combo.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchlate = StringVar()#biến giá trị tìm kiếm
        self.searchtc_entry = ttk.Entry(self.late_group, textvariable=self.var_searchlate, width=13,
                                   font=("times new roman", 10, "bold"))
        self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
        
        #nút tìm kiếm
        img_btn3 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn3 = img_btn3.resize((80, 30), PIL.Image.ANTIALIAS)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)
        searchtc_btn = Button(self.late_group, text="Search",
                              font=("times new roman", 10, "bold"), command=self.search_Latedata,
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=80, image=self.photobtn3, fg="white", compound="center")
        searchtc_btn.grid(row=0, column=2, padx=5)
        
        #Xem tất cả hs đi muộn
        showAlltc_btn = Button(self.late_group, text="Show all",
                               font=("times new roman", 10, "bold"),command=self.fetch_Latedata,
                               bd=0, bg="white", cursor='hand2', activebackground='white',
                               width=80, image=self.photobtn3, fg="white", compound="center"
                               )
        showAlltc_btn.grid(row=0, column=3, padx=5)
        
        #xuất ra file csv 
        exportLate_btn = Button(self.late_group, text="Export CSV",
                               font=("times new roman", 10, "bold"), command=self.exportCsv,
                                bd=0, bg="white", cursor='hand2', activebackground='white',
                                width=80, image=self.photobtn3, fg="white", compound="center")
        exportLate_btn.grid(row=0, column=4, padx=10)

        # bảng dữ liệu các học sinh đi muộn
        tabletc_frame = Frame(self.late_group, bd=2, relief=RIDGE, bg="white")
        tabletc_frame.place(x=10, y=38, width=600, height=155)

        # scroll bar
        scroll_x = ttk.Scrollbar(tabletc_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tabletc_frame, orient=VERTICAL)
        
        #các trường dữ liệu
        self.LateTable = ttk.Treeview(tabletc_frame, column=(
            "studentid", "name","class","date","lessonid", "status"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.LateTable.xview)
        scroll_y.config(command=self.LateTable.yview)
        
        #gán tên cấc cột
        self.LateTable.heading("studentid", text="Student ID")
        self.LateTable.heading("name", text="Student name")
        self.LateTable.heading("class", text="Class")
        self.LateTable.heading("date", text="Date")

        self.LateTable.heading("lessonid", text="Lesson ID")
        self.LateTable.heading("status", text="Status")
        
        #độ dài các cột
        self.LateTable["show"] = "headings"
        self.LateTable.column("studentid", width=100)
        self.LateTable.column("name", width=100)
        self.LateTable.column("date", width=100)
        self.LateTable.column("class", width=100)

        self.LateTable.column("lessonid", width=100)
        self.LateTable.column("status", width=100)

        self.LateTable.pack(fill=BOTH, expand=1)
        
        #hàm hiển thị tất cả hs đi muộn
        self.fetch_Latedata()

        #===========under-left===============
        #danh sách học sinh vắng= có điểm danh nhưng đi quá muộn
        self.noatt_group = LabelFrame(Left_frame, bd=1, bg="white", text="Absent students",
                                font=("times new roman", 10, "bold"), fg="black", relief=RIDGE)
        self.noatt_group.place(x=0, y=235, width=630, height=220)

        self.var_com_searchnoatt = StringVar()#biến loại điểm danh
        search_combo1 = ttk.Combobox(self.noatt_group, font=("times new roman", 10, "bold"),
                                    textvariable=self.var_com_searchnoatt,
                                    state="read only",
                                    width=12)
        search_combo1["values"] = ("Student ID", "Date","Lesson ID","Class")
        search_combo1.current(0)
        search_combo1.bind("<<ComboboxSelected>>", self.callbackTooLate)
        search_combo1.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchnoatt = StringVar()#biến giá trị tìm kiếm
        self.searchnoatt_entry = ttk.Entry(self.noatt_group, textvariable=self.var_searchnoatt, width=13,
                                   font=("times new roman", 10, "bold"))
        self.searchnoatt_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)

        searchnoatt_btn = Button(self.noatt_group, text="Search",
                              font=("times new roman", 10, "bold"),command=self.search_Notdata,
                                 bd=0, bg="white", cursor='hand2', activebackground='white',
                                 width=80, image=self.photobtn3, fg="white", compound="center")
        searchnoatt_btn.grid(row=0, column=2, padx=5)

        showAllnoatt_btn = Button(self.noatt_group, text="Show all",
                               font=("times new roman", 10, "bold"),command=self.fetch_Notdata,
                                  bd=0, bg="white", cursor='hand2', activebackground='white',
                                  width=80, image=self.photobtn3, fg="white", compound="center")
        showAllnoatt_btn.grid(row=0, column=3, padx=5)

        exportNoatt_btn = Button(self.noatt_group, text="Export CSV",
                                font=("times new roman", 10, "bold"), command=self.exportUnpresetCsv,
                                 bd=0, bg="white", cursor='hand2', activebackground='white',
                                 width=80, image=self.photobtn3, fg="white", compound="center")
        exportNoatt_btn.grid(row=0, column=4, padx=10)

        # table_frame
        tableatt_frame = Frame(self.noatt_group, bd=2, relief=RIDGE, bg="white")
        tableatt_frame.place(x=10, y=38, width=600, height=155)

        # scroll bar
        scroll_x = ttk.Scrollbar(tableatt_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tableatt_frame, orient=VERTICAL)

        self.NoAttTable = ttk.Treeview(tableatt_frame, column=(
            "studentid", "name","class", "date", "lessonid", "status"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.NoAttTable.xview)
        scroll_y.config(command=self.NoAttTable.yview)

        self.NoAttTable.heading("studentid", text="Student ID")
        self.NoAttTable.heading("name", text="Student name")
        self.NoAttTable.heading("class", text="Class")
        self.NoAttTable.heading("date", text="Date")

        self.NoAttTable.heading("lessonid", text="Lesson ID")
        self.NoAttTable.heading("status", text="Status")

        self.NoAttTable["show"] = "headings"
        self.NoAttTable.column("studentid", width=100)
        self.NoAttTable.column("name", width=100)
        self.NoAttTable.column("class", width=100)
        self.NoAttTable.column("date", width=100)

        self.NoAttTable.column("lessonid", width=100)
        self.NoAttTable.column("status", width=100)

        self.NoAttTable.pack(fill=BOTH, expand=1)
        self.fetch_Notdata()
        # self.LateTable.bind("<ButtonRelease>", self.get_cursorLate)

        #===================right_label====================
        #danh sách sinh viên ko điểm danh (ko đi qua camera)
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                font=("times new roman", 12, "bold"))
        Right_frame.place(x=670, y=125, width=615, height=470)

        noatt_lbl = Label(Right_frame, bd=0, bg="white", text="Students who did not check-in", font=("times new roman", 12, "bold"),
                         fg="red2", )
        noatt_lbl.place(x=0, y=0, width=600, height=30)

        self.notinGroup=LabelFrame(Right_frame,bd=0,bg="white")
        self.notinGroup.place(x=0,y=35,width=600,height=420)
        self.var_com_searchNotin = StringVar()#biến loại tìm kiếm
        search_combo2 = ttk.Combobox(self.notinGroup, font=("times new roman", 12, "bold"),
                                    textvariable=self.var_com_searchNotin,
                                    state="read only",
                                    width=12)
        search_combo2["values"] = ("Student ID", "Date", "Lesson ID","Class")
        search_combo2.current(0)
        search_combo2.bind("<<ComboboxSelected>>", self.callbackAbsent)#sự kiện khi chọn loại tìm kiếm
        search_combo2.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchNotin = StringVar()
        self.searchtc_entry = ttk.Entry(self.notinGroup, textvariable=self.var_searchNotin, width=13,
                                   font=("times new roman", 11, "bold"))
        self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
        #btn tìm
        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn2 = img_btn2.resize((100, 30), PIL.Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        searchtc_btn = Button(self.notinGroup, text="Search",
                              font=("times new roman", 11, "bold"),
                              command=self.search_Notindata,
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=100, image=self.photobtn2, fg="white", compound="center")
        searchtc_btn.grid(row=0, column=2, padx=5)

        showAlltc_btn = Button(self.notinGroup, text="Show all",
                               font=("times new roman", 11, "bold"), command=self.fetch_Notindata,
                               bd=0, bg="white", cursor='hand2', activebackground='white',
                               width=100, image=self.photobtn2, fg="white", compound="center")
        showAlltc_btn.grid(row=0, column=3, padx=5)

        exportLate_btn = Button(self.notinGroup, text="Export CSV",
                                font=("times new roman", 11, "bold"), command=self.exportNotinCsv,
                                bd=0, bg="white", cursor='hand2', activebackground='white',
                                width=100, image=self.photobtn2, fg="white", compound="center")
        exportLate_btn.grid(row=0, column=4, padx=5)

        # table_frame
        tablenotin_frame = Frame(self.notinGroup, bd=2, relief=RIDGE, bg="white")
        tablenotin_frame.place(x=10, y=38, width=585, height=375)

        # scroll bar
        scroll_x = ttk.Scrollbar(tablenotin_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablenotin_frame, orient=VERTICAL)

        self.NotInTable = ttk.Treeview(tablenotin_frame, column=(
            "studentid", "name","class", "date", "lessonid","status"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.NotInTable.xview)
        scroll_y.config(command=self.NotInTable.yview)

        self.NotInTable.heading("studentid", text="Student ID")
        self.NotInTable.heading("name", text="Student name")
        self.NotInTable.heading("class", text="Class")
        self.NotInTable.heading("date", text="Date")
        self.NotInTable.heading("lessonid", text="Lesson ID")
        self.NotInTable.heading("status", text="Status")


        self.NotInTable["show"] = "headings"
        self.NotInTable.column("studentid", width=100)
        self.NotInTable.column("name", width=100)
        self.NotInTable.column("class", width=100)
        self.NotInTable.column("date", width=100)

        self.NotInTable.column("lessonid", width=100)


        self.NotInTable.pack(fill=BOTH, expand=1)
        self.fetch_Notindata()


    def callbackLate(self,event):#hàm chuyển đổi txtbox khi chọn loại điểm danh
        mls = event.widget.get()
        if(mls=='Date'):#loại điểm danh là theo Ngày thì chuyển về dạng DateEntry
            self.searchtc_entry=DateEntry(self.late_group, width=13, bd=0, selectmode='day',textvariable=self.var_searchlate,
                  year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 10),
                  day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)


        else:
            self.searchtc_entry = ttk.Entry(self.late_group, textvariable=self.var_searchlate, width=14,
                                        font=("times new roman", 10, "bold"))
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
            self.var_searchlate.set("")
            
    def callbackTooLate(self,event1):#hàm chuyển đổi txtbox khi chọn loại điểm danh
        mls = event1.widget.get()
        if(mls=='Date'):#loại điểm danh là theo Ngày thì chuyển về dạng DateEntry
            self.searchnoatt_entry=DateEntry(self.noatt_group, width=13, bd=0, selectmode='day',textvariable=self.var_searchnoatt,
                  year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 10),
                  day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
            self.searchnoatt_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)


        else:
            self.searchnoatt_entry = ttk.Entry(self.noatt_group, textvariable=self.var_searchnoatt, width=14,
                                        font=("times new roman", 10, "bold"))
            self.searchnoatt_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
            self.var_searchnoatt.set("")
    
    #ko điểm danh
    def callbackAbsent(self,event1):#hàm chuyển đổi txtbox khi chọn loại điểm danh
        mls = event1.widget.get()
        if(mls=='Date'):#loại điểm danh là theo Ngày thì chuyển về dạng DateEntry
            self.searchtc_entry=DateEntry(self.notinGroup, width=14, bd=0, selectmode='day',textvariable=self.var_searchNotin,
                  year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 10),
                  day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)


        else:
            self.searchtc_entry = ttk.Entry(self.notinGroup, textvariable=self.var_searchNotin, width=15,
                                        font=("times new roman", 10, "bold"))
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
            self.var_searchNotin.set("")

        

    def fetch_Latedata(self):
            # global mydata
            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            attendance_collection = db["attendance"]
            pipeline = [
                {
                    "$match": {
                        "AttendanceStatus": {"$regex": "Late"}
                    }
                },
                {
                    "$lookup": {
                        "from": "lesson",
                        "localField": "Lesson_id",
                        "foreignField": "Lesson_id",
                        "as": "lesson_info"
                    }
                },
                {
                    "$lookup": {
                        "from": "student",
                        "localField": "Student_id",
                        "foreignField": "Student ID",
                        "as": "student_info"
                    }
                },
                {
                    "$project": {
                        "Student_id": "$Student_id",
                        "Name": "$Name",
                        "class": "$class",
                        "Date": "$Date",
                        "Lesson_id": "Lesson_id",
                        "AttendanceStatus": "$AttendanceStatus"
                    }
                }
            ]

            data = attendance_collection.aggregate(pipeline)
            insert_data = []  # 用來存放擷取到的資料
            for document in data:
                # 將每個文件的資料轉換成元組並添加到data中
                class_data = (
                    document["Student_id"],
                    document["Name"],
                    document["class"],
                    document["Date"],
                    document["Lesson_id"],
                    document["AttendanceStatus"],

                )
                insert_data.append(class_data)

            print(insert_data)

            if len(insert_data) > -1:
                self.LateTable.delete(*self.LateTable.get_children())
                for i in insert_data:
                    self.LateTable.insert("", END, values=i)
                    mydata.append(i)

    def search_Latedata(self):
        if self.var_com_searchlate.get()=="" or self.var_searchlate.get()=="":
            messagebox.showerror("Error!","Please enter complete information",parent=self.root)

        else:
            print(self.var_searchlate.get())
            try:
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                # 指定集合（collection）
                attendance_collection = db["attendance"]

                if(self.var_com_searchlate.get()=="Student ID"):
                    self.var_com_searchlate.set("student.Student_id")
                elif(self.var_com_searchlate.get()=="Date"):
                    self.var_com_searchlate.set("attendance.Date")
                elif (self.var_com_searchlate.get() == "Class"):
                    self.var_com_searchlate.set("student.Class")
                else:
                    if(self.var_com_searchlate.get()=="Lesson ID"):
                        self.var_com_searchlate.set("lesson.Lesson_id")

                mydata.clear()
                pipeline = [
                    {
                        "$match": {
                            "AttendanceStatus": {"$regex": "Late attendance"}
                        }
                    },
                    {
                        "$lookup": {
                            "from": "lesson",
                            "localField": "Lesson_id",
                            "foreignField": "Lesson_id",
                            "as": "lesson_info"
                        }
                    },
                    {
                        "$lookup": {
                            "from": "student",
                            "localField": "Student_id",
                            "foreignField": "Student ID",
                            "as": "student_info"
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "Student_id": "$student_info.Student ID",
                            "Name": "$student_info.Student name",
                            "Class": "$student_info.Course",
                            "Date": "$Date",
                            "Lesson_id": "$lesson_info.Lesson_id",
                            "AttendanceStatus": "$AttendanceStatus"
                        }
                    }
                ]

                data = attendance_collection.aggregate(pipeline)

                insert_data = []  # 用來存放擷取到的資料
                for document in data:
                    # 將每個文件的資料轉換成元組並添加到data中
                    class_data = (
                        document["Student_id"],
                        document["Name"],
                        document["class"],
                        document["Date"],
                        document["Lesson_id"],
                        document["AttendanceStatus"]

                    )
                    insert_data.append(class_data)

                print(insert_data)

                if(len(insert_data)!=0):
                    self.LateTable.delete(*self.LateTable.get_children())
                    for i in insert_data:
                        self.LateTable.insert("",END,values=i)
                        mydata.append(i)
                    messagebox.showinfo("Notification","Yes"+str(len(insert_data))+"records that meet the condition",parent=self.root)

                else:
                    self.LateTable.delete(*self.LateTable.get_children())
                    messagebox.showinfo("Notification", "No records meet the condition",parent=self.root)
                client.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
    def exportCsv(self):
        try:
            # 连接到 MongoDB
            client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            student_collection = db["student"]

            # 从 MongoDB 中检索学生数据
            cursor = student_collection.find()
            records = list(cursor)

            current_GMT = time.gmtime()

            # ts stores timestamp
            ts = calendar.timegm(current_GMT)

            if len(records) < 1:
                messagebox.showerror("No data","No data to export file",parent=self.root)
                return False

            # 将学生数据写入 CSV 文件
            with open('late_export' + str(ts) + '_' + str(self.today) + '.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['Student ID', 'Name', 'class', 'Date', 'Lesson_id', 'AttendanceStatus'])
                for record in records:
                    writer.writerow([
                        record.get("Student ID", ""),
                        record.get("Name", ""),
                        record.get("class", ""),
                        record.get("Date", ""),
                        record.get("Lesson_id", ""),
                        record.get("AttendanceStatus", "")

                    ])

            client.close()

            messagebox.showinfo("Export data", "Your data has been successfully exported!")
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    #===================No ATT=========================
    def fetch_Notdata(self):
            # global mydata
            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            attendance_collection = db["attendance"]
            pipeline = [
                {
                    "$match": {
                        "AttendanceStatus": {"$regex": "Absent"}
                    }
                },
                {
                    "$lookup": {
                        "from": "lesson",
                        "localField": "Lesson_id",
                        "foreignField": "Lesson_id",
                        "as": "lesson_info"
                    }
                },
                {
                    "$lookup": {
                        "from": "student",
                        "localField": "Student_id",
                        "foreignField": "Student ID",
                        "as": "student_info"
                    }
                },
                {
                    "$project": {
                        "Student_id": "$student_info.Student ID",
                        "Name": "$student_info.Student name",
                        "Class": "$student_info.Course",
                        "Date": "$Date",
                        "Lesson_id": "$lesson_info.Lesson_id",
                        "AttendanceStatus": "$AttendanceStatus"
                    }
                }
            ]
            data = attendance_collection.aggregate(pipeline)
            insert_data = []  # 用來存放擷取到的資料
            for document in data:
                # 將每個文件的資料轉換成元組並添加到data中
                class_data = (
                    document["Student_id"],
                    document["Name"],
                    document["Class"],
                    document["Date"],
                    document["Lesson_id"],
                    document["AttendanceStatus"]

                )
                insert_data.append(class_data)

            print(insert_data)
            mydataNot.clear()

            if len(insert_data) != 0:
                self.NoAttTable.delete(*self.NoAttTable.get_children())
                for i in insert_data:
                    self.NoAttTable.insert("", END, values=i)
                    mydataNot.append(i)
            client.close()
    def search_Notdata(self):
        if self.var_com_searchnoatt.get()=="" or self.var_searchnoatt.get()=="":
            messagebox.showerror("Error!","Error! Please enter full information",parent=self.root)

        else:
            print(self.var_searchnoatt.get())
            try:
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                # 指定集合（collection）
                attendance_collection = db["attendance"]


                if(self.var_com_searchnoatt.get()=="Student ID"):
                    self.var_com_searchnoatt.set("student_info.Student ID")
                elif(self.var_com_searchnoatt.get()=="Date"):
                    self.var_com_searchnoatt.set("attendance.Date")
                elif (self.var_com_searchnoatt.get() == "Class"):
                    self.var_com_searchnoatt.set("student_info.Course")
                else:
                    if(self.var_com_searchnoatt.get()=="Lesson ID"):
                        self.var_com_searchnoatt.set("lesson.Lesson_id")

                mydataNot.clear()
                pipeline = [
                    {
                        "$match": {
                            "AttendanceStatus": {"$regex": "Absent"},
                            "Lesson_id": {"$eq": self.var_com_searchnoatt.get()}
                        }
                    },
                    {
                        "$lookup": {
                            "from": "lesson",
                            "localField": "Lesson_id",
                            "foreignField": "Lesson_id",
                            "as": "lesson_info"
                        }
                    },
                    {
                        "$unwind": "$lesson_info"
                    },
                    {
                        "$lookup": {
                            "from": "student",
                            "localField": "Student_id",
                            "foreignField": "Student ID",
                            "as": "student_info"
                        }
                    },
                    {
                        "$unwind": "$student_info"
                    },
                    {
                        "$project": {
                            "Student_id": "$Student_id",
                            "Name": "$Name",
                            "Class": "$class",
                            "Date": "$Date",
                            "Lesson_id": "$Lesson_id",
                            "AttendanceStatus": "$AttendanceStatus"
                        }
                    }
                ]

                data = attendance_collection.aggregate(pipeline)

                insert_data = []  # 用來存放擷取到的資料
                for document in data:
                    # 將每個文件的資料轉換成元組並添加到data中
                    class_data = (
                        document["Student_id"],
                        document["Name"],
                        document["Class"],
                        document["Date"],
                        document["Lesson_id"],
                        document["AttendanceStatus"]

                    )
                    insert_data.append(class_data)

                print(insert_data)

                if(len(insert_data)!=0):
                    self.NoAttTable.delete(*self.NoAttTable.get_children())
                    for i in data:
                        self.NoAttTable.insert("",END,values=i)
                        mydataNot.append(i)
                    messagebox.showinfo("Notification","Yes "+str(len(insert_data))+"records match the condition",parent=self.root)

                else:
                    self.NoAttTable.delete(*self.NoAttTable.get_children())
                    messagebox.showinfo("Notification", "No records match the conditions",parent=self.root)
                client.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
    def exportUnpresetCsv(self):
        try:
            # 连接到 MongoDB
            client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            attendance_collection = db["attendance"]

            # 从 MongoDB 中检索学生数据
            cursor = attendance_collection.find()
            records = list(cursor)

            current_GMT = time.gmtime()
            ts = calendar.timegm(current_GMT)

            # 将学生数据写入 CSV 文件
            with open('Absent_export' + str(ts) + '_' + str(
                    self.today) + '.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['Student ID', 'Name', 'class', 'Date', 'Lesson_id', 'AttendanceStatus'])
                for record in records:
                    writer.writerow([
                        record.get("Student ID", ""),
                        record.get("Name", ""),
                        record.get("class", ""),
                        record.get("Date", ""),
                        record.get("Lesson_id", ""),
                        record.get("AttendanceStatus", "")

                    ])


            messagebox.showinfo("Export Data", "The data has been exported to the Attendance_CSV folder!")
            client.close()



        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    #===========================NOT IN ATT============================
    def fetch_Notindata(self):
            # global mydata
            mydataNotInAtt.clear()
            client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            attendance_collection = db["attendance"]
            pipeline = [
                {
                    "$lookup": {
                        "from": "class",
                        "localField": "Class",
                        "foreignField": "Class",
                        "as": "class_info"
                    }
                },
                {
                    "$unwind": "$class_info"
                },
                {
                    "$lookup": {
                        "from": "lesson",
                        "localField": "class_info.Class",
                        "foreignField": "Class",
                        "as": "lesson_info"
                    }
                },
                {
                    "$unwind": "$lesson_info"
                },
                {
                    "$project": {
                        "_id": 0,
                        "Student_id": "$Student_id",
                        "Name": "$Name",
                        "Class": "$Class",
                        "Date": "$lesson_info.Date",
                        "Lesson_id": "$lesson_info.Lesson_id",
                        "attendance_info": "$attendance_info"  # 將現有的 attendance_info 保留，以便後續使用
                    }
                },
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                {
                                    "$not": {
                                        "$in": [
                                            {"$concat": ["$Student_id", "$Lesson_id"]},
                                            {
                                                "$map": {
                                                    "input": "$attendance_info",
                                                    "as": "att",
                                                    "in": {"$concat": ["$$att.Student_id", "$$att.Lesson_id"]}
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "$lte": [
                                        {"$dateFromString": {"dateString": "$Date", "format": "%d/%m/%Y"}},
                                        {"$dateFromString": {"dateString": self.today_time, "format": "%d/%m/%Y"}}
                                    ]
                                },
                                {
                                    "$not": {
                                        "$regexMatch": {
                                            "input": {"$toString": "$Class"},
                                            "regex": self.var_com_searchNotin.get()
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            ]

            data = attendance_collection.aggregate(pipeline)
            insert_data = []  # 用來存放擷取到的資料
            for document in data:
                # 將每個文件的資料轉換成元組並添加到data中
                class_data = (
                    document["Student_id"],
                    document["Name"],
                    document["class"],
                    document["Date"],
                    document["Class"],
                    document["Lesson_id"]

                )
                insert_data.append(class_data)

            print(insert_data)

            if len(insert_data) > -1:
                self.NotInTable.delete(*self.NotInTable.get_children())
                for i in insert_data:
                    self.NotInTable.insert("", END, values=i)
                    mydataNotInAtt.append(i)
            client.close()

    def search_Notindata(self):
        if self.var_com_searchNotin.get()=="" or self.var_searchNotin.get()=="":
            messagebox.showerror("Error!","Please enter complete information.",parent=self.root)

        else:
            try:
                client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                db = client["Face_Recognizer"]
                attendance_collection = db["attendance"]

                if(self.var_com_searchNotin.get()=="Student ID"):
                    self.var_com_searchNotin.set("student.Student ID")
                elif(self.var_com_searchNotin.get()=="Date"):
                    self.var_com_searchNotin.set("Date")

                elif (self.var_com_searchNotin.get() == "Class"):
                    self.var_com_searchNotin.set("student.Course")
                else:
                    if(self.var_com_searchNotin.get()=="Lesson ID"):
                        self.var_com_searchNotin.set("Lesson_id")

                mydataNotInAtt.clear()
                pipeline = [
                    {
                        "$lookup": {
                            "from": "class",
                            "localField": "Class",
                            "foreignField": "Class",
                            "as": "class_info"
                        }
                    },
                    {
                        "$unwind": "$class_info"
                    },
                    {
                        "$lookup": {
                            "from": "lesson",
                            "localField": "class_info.Class",
                            "foreignField": "Class",
                            "as": "lesson_info"
                        }
                    },
                    {
                        "$unwind": "$lesson_info"
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "Student_id": "$Student_id",
                            "Name": "$Name",
                            "Class": "$class",
                            "Date": "$lesson_info.Date",
                            "Lesson_id": "$lesson_info.Lesson_id"
                        }
                    },
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {
                                        "$not": {
                                            "$in": [
                                                {"$concat": ["$Student_id", "$Lesson_id"]},
                                                {
                                                    "$map": {
                                                        "input": {
                                                            "$filter": {
                                                                "input": "$attendance_info",
                                                                "as": "att",
                                                                "cond": {
                                                                    "$eq": [
                                                                        {"$concat": ["$$att.Student_id",
                                                                                     "$$att.Lesson_id"]},
                                                                        {"$concat": ["$Student_id", "$Lesson_id"]}
                                                                    ]
                                                                }
                                                            }
                                                        },
                                                        "as": "result",
                                                        "in": {"$concat": ["$$result.Student_id", "$$result.Lesson_id"]}
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "$lte": [
                                            {"$dateFromString": {"dateString": "$Date", "format": "%d/%m/%Y"}},
                                            {"$dateFromString": {"dateString": self.today_time, "format": "%d/%m/%Y"}}
                                        ]
                                    },
                                    {
                                        "$regexMatch": {
                                            "input": {"$toString": "$Class"},
                                            "regex": self.var_com_searchNotin.get()
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]

                data = attendance_collection.aggregate(pipeline)
                insert_data = []  # 用來存放擷取到的資料
                for document in data:
                    # 將每個文件的資料轉換成元組並添加到data中
                    class_data = (
                        document["Student_id"],
                        document["Name"],
                        document["Class"],
                        document["Date"],
                        document["Lesson_id"]

                    )
                    insert_data.append(class_data)

                print(insert_data)

                if len(insert_data) != 0:
                    self.NotInTable.delete(*self.NotInTable.get_children())
                    for i in insert_data:
                        self.NotInTable.insert("", END, values=i)
                        mydataNotInAtt.append(i)
                    messagebox.showinfo("Notification", "Yes "+str(len(insert_data)) + " records satisfy the conditions", parent=self.root)

                else:
                    self.NotInTable.delete(*self.NotInTable.get_children())
                    messagebox.showinfo("Notification", " No records satisfy the conditions", parent=self.root)
                client.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
    def exportNotinCsv(self):
        try:

            if len(mydataNotInAtt)<1:
                messagebox.showerror("No data","There is no data to export",parent=self.root)
                return False

            # 连接到 MongoDB
            client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            attendance_collection = db["attendance"]

            # 从 MongoDB 中检索学生数据
            cursor = attendance_collection.find()
            records = list(cursor)

            # Current GMT time in a tuple format
            current_GMT = time.gmtime()

            # ts stores timestamp
            ts = calendar.timegm(current_GMT)

            # 将学生数据写入 CSV 文件
            with open('Not-check in_export' + str(ts)+'_'+str(self.today)+'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['Student_id', 'Name', 'class', 'Date', 'Lesson_id', 'AttendanceStatus'])
                for record in records:
                    writer.writerow([
                        record.get("Student_id", ""),
                        record.get("Name", ""),
                        record.get("class", ""),
                        record.get("Date", ""),
                        record.get("Lesson_id", ""),
                        record.get("AttendanceStatus", "")

                    ])

            messagebox.showinfo("Export Data","Your data has been exported to the Not-check in csv file!")
            client.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due to：{str(es)}", parent=self.root)


if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Report(root)
    root.mainloop()# cua so hien len