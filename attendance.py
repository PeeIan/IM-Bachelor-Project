import datetime
import os
from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
from tkinter import messagebox
import pandas as pd
import chardet
import mysql.connector
import numpy as np
from PIL import ImageTk
import cv2
from time import strftime
import csv
from tkinter import filedialog
from database_str import Database_str
import pymongo
from pymongo import MongoClient

mydata=[]# mảng data
class Attendance:

    def __init__(self,root):
        self.root=root
        w = 1350#chiều dài giao diện
        h = 700#chiều rộng giao diện

        ws = self.root.winfo_screenwidth()#độ dài màn hình
        hs = self.root.winfo_screenheight()#độ rộng màn
        x = (ws / 2) - (w / 2) #vị trí cách lề trái x px
        y = (hs / 2) - (h / 2) #vị trí cách lề trên y px

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y)) #kích thước và vị trí hiển thị giao diện
        self.root.title("Attendance Management")#tiêu đề
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')#icon giao diện
        self.isClicked=False # biến đã chọn
        today = strftime("%d-%m-%Y")#ngày hôm nay
        self.today=strftime("%d-%m-%Y")
        
        self.db=Database_str()#thông tin kết nối database

        #===========variables=========
        self.var_atten_id=StringVar() #biến kiểu string(chuỗi ký tự) id điểm danh
        self.var_atten_class = StringVar()#lớp học
        self.var_atten_idsv = StringVar()#id học sinh
        self.var_atten_name = StringVar() #tên học sinh
        self.var_atten_timein = StringVar()#thời gian vào
        self.var_atten_timeout = StringVar()#thời gian ra
        self.var_atten_date = StringVar()#ngày
        self.var_atten_attendance = StringVar()#trạng thái
        self.var_atten_lesson=StringVar()#lesson id

        #ảnh nền resize
        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")#mở ảnh trong thư mục
        img3 = img3.resize((1350, 700), PIL.Image.ANTIALIAS)# chỉnh kích thước ảnh về 1350x700
        self.photoimg3 = ImageTk.PhotoImage(img3)#ép kiểu về ImageTk

        #khai báo label chứa ảnh nền
        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1350, height=700)#(x=0: cách lề trái 0px, y=0: cách lề trên 0px, width: chiều dài 1350px, height: chiều cao)

        # ==================================heading====================================
        # ====time====
        #hiển thị thời gian hiện tại
        #ảnh thời gian
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")#mở ảnh 
        img_time = img_time.resize((27, 27), PIL.Image.ANTIALIAS)#resize ảnh về kích thước 27x27
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime, bg="white")
        time_img.place(x=43, y=40, width=27, height=27)

        def time():#hàm thay đổi thời gian mỗi 1 giây
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(self.root, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl.place(x=80, y=35, width=100, height=20)
        time()#chạy hàm time
        lbl1 = Label(self.root, text=today, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=20)

        # ====title=========
        self.txt = "Attendance Information Management"
        self.count = 0
        # self.text = ''
        # self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 22, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=350, y=22, width=600)

        #frame chính và vị trí
        main_frame = Frame(bg_img, bd=2, bg="white")# nằm trong label bg_img, viền xung quanh 2px, bg: mầu nền trắng
        main_frame.place(x=24, y=90, width=1293, height=586)

        # frame bên trái chứa các label, entry textbox
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=5, width=390, height=580)

        # text cập nhật điiểm danh
        label_Update_att=Label(Left_frame,bg="#F0FFF0",fg="#483D8B",text="Update Attendance",font=("times new roman", 18, "bold"))
        label_Update_att.place(x=0, y=1, width=386, height=35)

        left_inside_frame = Frame(Left_frame, bd=1, bg="white")
        left_inside_frame.place(x=0, y=60, width=380, height=500)

        #id điểm danh
        auttendanceID_label = Label(left_inside_frame, text="Attendance ID:", font=("times new roman", 12, "bold"),
                                bg="white")
        auttendanceID_label.grid(row=0, column=0, padx=20, pady=5, sticky=W)
        #entry để nhập id điểm danh
        auttendanceID_entry = ttk.Entry(left_inside_frame,textvariable=self.var_atten_id,
                                    font=("times new roman", 12, "bold"),state="readonly")
        auttendanceID_entry.grid(row=0, column=1, padx=20, pady=5, sticky=W)


        #id học sinh
        roll_label = Label(left_inside_frame, text="Student ID:", font=("times new roman", 12, "bold"),
                                    bg="white")
        roll_label.grid(row=1, column=0, padx=20, pady=5, sticky=W)
        #nhập tên học sinh
        roll_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_idsv,
                                        font=("times new roman", 12, "bold"),state="readonly")
        roll_entry.grid(row=1, column=1, padx=20, pady=5, sticky=W)



        #tên hs
        nameLabel = Label(left_inside_frame, text="Student Name:", font=("times new roman", 12, "bold"),
                                    bg="white")
        nameLabel.grid(row=2, column=0, padx=20, pady=5, sticky=W)

        nameLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_name,
                                        font=("times new roman", 12, "bold"),state="readonly")
        nameLabel_entry.grid(row=2, column=1, padx=20, pady=5, sticky=W)



        #lớp
        classLabel = Label(left_inside_frame, text="Classroom:", font=("times new roman", 12, "bold"),
                                    bg="white")
        classLabel.grid(row=3, column=0, padx=20, pady=5, sticky=W)

        classLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_class,
                                        font=("times new roman", 12, "bold"),state="readonly")
        classLabel_entry.grid(row=3, column=1, padx=20, pady=5, sticky=W)

        #thời gian vào
        timeLabel = Label(left_inside_frame, text="Check-in Time:", font=("times new roman", 12, "bold"),
                                    bg="white")
        timeLabel.grid(row=4, column=0, padx=20, pady=5, sticky=W)

        timeLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_timein,
                                        font=("times new roman", 12, "bold"))
        timeLabel_entry.grid(row=4, column=1, padx=20, pady=5, sticky=W)

        # thời gian ra
        timeoutLabel = Label(left_inside_frame, text="Check-out Time:", font=("times new roman", 12, "bold"),
                          bg="white")
        timeoutLabel.grid(row=5, column=0, padx=20, pady=5, sticky=W)

        timeoutLabel_entry = ttk.Entry(left_inside_frame, width=20, textvariable=self.var_atten_timeout,
                                    font=("times new roman", 12, "bold"))
        timeoutLabel_entry.grid(row=5, column=1, padx=20, pady=5, sticky=W)

        #ngày
        dateLabel = Label(left_inside_frame, text="Date:", font=("times new roman", 12, "bold"),
                          bg="white")
        dateLabel.grid(row=6, column=0, padx=20, pady=5, sticky=W)

        dateLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_date,
                                    font=("times new roman", 12, "bold"),state="readonly")
        dateLabel_entry.grid(row=6, column=1, padx=20, pady=5, sticky=W)

        #trạng thái
        auttendanceLabel = Label(left_inside_frame, text="Attendance:", font=("times new roman", 12, "bold"),
                           bg="white")
        auttendanceLabel.grid(row=7, column=0,  padx=20, pady=5, sticky=W)

        self.atten_status=ttk.Entry(left_inside_frame    ,width=20,font=("times new roman", 12, "bold"),textvariable=self.var_atten_attendance)

        self.atten_status.grid(row=7,column=1,pady=5,padx=20)



        #id bài học
        lessonLabel = Label(left_inside_frame, text="Lesson ID:", font=("times new roman", 12, "bold"),
                                 bg="white")
        lessonLabel.grid(row=8, column=0, padx=20, pady=5, sticky=W)

        self.lesson = ttk.Entry(left_inside_frame, width=20, font=("times new roman", 12, "bold"),
                                         state="readonly", textvariable=self.var_atten_lesson)
        self.lesson.grid(row=8, column=1, pady=5, padx=20)



        # btn_frame
        #ảnh nút đỏ
        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn2 = img_btn2.resize((220, 35), PIL.Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        #nút xem ảnh
        label_Update_att = Button(Left_frame, text="Preview Image",command=self.openImage,
                                 font=("times new roman", 12, "bold"),bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=220,image=self.photobtn2,fg="white",compound="center")
        label_Update_att.place(x=80, y=480, width=220, height=35)
        #nút xóa ảnh
        update_btn = Button(Left_frame, text="Remove", command=self.delete_data,
                            font=("times new roman", 12, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=220, image=self.photobtn2, fg="white", compound="center")
        update_btn.place(x=80, y=530,width=220,height=35 )

        #frame chứa các nút nhỏ
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn1 = img_btn1.resize((150, 35), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        btn_frame = Frame(left_inside_frame, bg="white")
        btn_frame.place(x=0, y=320, width=400, height=105)

        #nhập file csv
        save_btn = Button(btn_frame, text="Import CSV file",command=self.importCsv ,font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=150,image=self.photobtn1,fg="white",compound="center")
        save_btn.grid(row=9, column=0,padx=20)

        #xuất ra file csv
        update_btn = Button(btn_frame, text="Export CSV file",command=self.exportCsv, font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        update_btn.grid(row=9, column=1,padx=20)

        #cập nhật thông tin điểm danh
        delete_btn = Button(btn_frame, text="Update",command=self.update_data ,font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        delete_btn.grid(row=10, column=0,pady=10)

        #làm mới
        reset_btn = Button(btn_frame, text="Refresh",command=self.reset_data, font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=150, image=self.photobtn1, fg="white", compound="center")
        reset_btn.grid(row=10, column=1,pady=10)




        #right_ label
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=410, y=5, width=880, height=580)


        #text tìm kiếm theo
        self.var_com_search=StringVar()# biến loại tìm kếm(theo ngày,id điểm danh,..) kiểu string(chuỗi ký tự)
        search_label = Label(Right_frame, text="Search By :", font=("times new roman", 11, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=15, pady=5, sticky=W)

        #chọn loại tìm kiếm
        search_combo = ttk.Combobox(Right_frame, font=("times new roman", 11, "bold"),textvariable=self.var_com_search, state="read only",
                                    width=13)
        search_combo["values"] = ("Attendance ID", "Date", "Student ID","Lesson Session ID")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=15, sticky=W)

        self.var_search=StringVar()#biến string nhập tìm kiếm
        search_entry = ttk.Entry(Right_frame,textvariable=self.var_search, width=15, font=("times new roman", 11, "bold"))
        search_entry.grid(row=0, column=2, padx=15, pady=5, sticky=W)

        #nút tìm kiếm
        img_btn3 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn3 = img_btn3.resize((110, 35), PIL.Image.ANTIALIAS)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)#ảnh nền màu đỏ bo tròn cho nút
        search_btn = Button(Right_frame,command=self.search_data, text="Search", font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=110,image=self.photobtn3,fg="white",compound="center")# nằm trong Right_frame, command( hàm để chạy chức năng tìm kiếm),fg: màu chữ, compound: vị trí hiển thị của chữ
        search_btn.grid(row=0, column=3, padx=15)

        #nút hiển thị hôm nay( hiển thị dữ liệu hôm nay)
        Today_btn = Button(Right_frame, text="Today",command=self.today_data, font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=110,image=self.photobtn3,fg="white",compound="center")
        Today_btn.grid(row=0, column=4, padx=15)

        #nút hiển thị tất cả dữ liệu
        showAll_btn = Button(Right_frame, text="Show All", command=self.fetch_data,font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=110,image=self.photobtn3,fg="white",compound="center")
        showAll_btn.grid(row=0, column=5, padx=15)


        #bảng dữ liệu
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=55, width=860, height=510)

        #scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable=ttk.Treeview(table_frame,column=("id","idsv","name","class","time_in","time_out","date","lesson","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        #đặt tên cột dữ liệu
        self.AttendanceReportTable.heading("id",text="Attendance ID")
        self.AttendanceReportTable.heading("idsv", text="Student ID")
        self.AttendanceReportTable.heading("name", text="Student name")
        self.AttendanceReportTable.heading("class", text="Classroom")
        self.AttendanceReportTable.heading("time_in", text="Check-in time")
        self.AttendanceReportTable.heading("time_out", text="Check-out time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Attendance")
        self.AttendanceReportTable.heading("lesson", text="Lesson ID")

        self.AttendanceReportTable["show"]="headings"#hiển thị tên cột lên bảng

        #cập nhật chiều dài các cột
        self.AttendanceReportTable.column("id",width=100)
        self.AttendanceReportTable.column("idsv", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("class", width=100)
        self.AttendanceReportTable.column("time_in", width=100)
        self.AttendanceReportTable.column("time_out", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)
        self.AttendanceReportTable.column("lesson", width=100)

        self.AttendanceReportTable.pack(fill=BOTH,expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)# bắt sự kiện khi click vào bảng dữ liệu
        self.fetch_data()  # load du lieu len grid
        #================fetchData======================

        # =======================fetch-data========================
    #hàm lấy tất cả dữ liệu
    def fetch_data(self):
            # global mydata
            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            attendance_collection = db["attendance"]
            data = attendance_collection.find({}, {"_id": 0})
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

            if len(insert_data) > -1:#nếu có dữ liệu
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())# xóa hết các phần tử cũ của bảng
                for i in insert_data:#với mỗi dòng dữ liệu trong data
                    self.AttendanceReportTable.insert("", END, values=i)#thêm dữ liệu lên bảng


            client.close()
    #update du lieu chuan hoa tren bang?:
    
    #import csv

    def importCsv(self):
        try:
            global mydata
            mydata.clear()
            fln = filedialog.askopenfilename(initialdir=os.getcwd() + "/ListCSV", title="Open CSV",
                                             filetypes=(("CSV File", ".csv"), ("ALL File", "*.*")), parent=self.root)
            print(fln)

            # Detect the encoding of the CSV file
            with open(fln, 'rb') as f:
                encoding = chardet.detect(f.read()).get('encoding')
                print(encoding)

            df = pd.read_csv(fln, encoding = encoding)

            for index, row in df.iterrows():
                mydata.append({
                    "IdAuttendance": row[0],
                    "Student_id": row[1],
                    "Name": str(row[2]),
                    "class": row[3],
                    "Time_in": row[4],
                    "Time_out": row[5],
                    "Date": row[6],
                    "Lesson_id": row[7],
                    "AttendanceStatus": row[8]

                })

            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            attendance_collection = db["attendance"]

            # 插入數據到 MongoDB
            attendance_collection.insert_many(mydata)

            messagebox.showinfo("Notification:", "Added student list successfully!")
            self.reset_data()
            self.fetch_data()
            client.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)


    #xuất dữ liệu ra excel
    def exportCsv(self):  # Python語法
        try:  # Python語法
            # -----------我是分隔線-------------#
            # 连接到 MongoDB
            client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            attendance_collection = db["attendance"]

            # 从 MongoDB 中检索学生数据
            cursor = attendance_collection.find()
            records = list(cursor)

            # 将学生数据写入 CSV 文件
            with open('Attendance_export.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['IdAuttendance', 'Student_id', 'Name', 'class', 'Time_in', 'Time_out', 'Date', 'Lesson_id',
                     'AttendanceStatus'])
                for record in records:
                    writer.writerow([
                        record.get("IdAuttendance", ""),
                        record.get("Student_id", ""),
                        record.get("Name", ""),
                        record.get("class", ""),
                        record.get("Time_in", ""),
                        record.get("Time_out", ""),
                        record.get("Date", ""),
                        record.get("Lesson_id", ""),
                        record.get("AttendanceStatus", "")
                    ])

            messagebox.showinfo("Export", "Attendance information derived successfully！", parent=self.root)
            client.close()
        except Exception as es:  # Python語法
            messagebox.showerror("Error", f"Due to：{str(es)}", parent=self.root)  # Tkinter套件


    def get_cursor(self,event=""):#hàm sự kiện click vào bảng
        cursor_row=self.AttendanceReportTable.focus()#chọn bảng
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']#lấy giá trị của dòng dữ liệu được click
        self.var_atten_id.set(rows[0])#set giá trị mã học sinh là vị trí 0 của mảng rows
        self.var_atten_idsv.set(rows[1])
        self.var_atten_name.set(rows[2])
        self.var_atten_class.set(rows[3])
        self.var_atten_timein.set(rows[4])
        self.var_atten_timeout.set(rows[5])
        self.var_atten_date.set(rows[6])
        self.var_atten_attendance.set(rows[8])
        self.var_atten_lesson.set(rows[7])

    def reset_data(self):#cài đặt lại các giá trị về rỗng
        self.var_atten_id.set("")
        self.var_atten_idsv.set("")
        self.var_atten_name.set("")
        self.var_atten_class.set("")
        self.var_atten_timein.set("")
        self.var_atten_timeout.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("Status")
        self.var_atten_lesson.set("Lesson")
    def update_data(self):#cập nhật dữ liệu
        if self.var_atten_lesson.get()=="Lesson" or self.var_atten_attendance.get()=="Status" or self.var_atten_id.get()=="":#nếu ko nhập đủ thông tin
            messagebox.showerror("Error","Please fill in all required fields.",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this record?",parent=self.root)#hiện thông báo hỏi có muốn cập nhật
                # 获取更新的数据
                atten_id = self.var_atten_id.get()
                student_id = self.var_atten_idsv.get()
                name = self.var_atten_name.get()
                class_name = self.var_atten_class.get()
                time_in = self.var_atten_timein.get()
                time_out = self.var_atten_timeout.get()
                date = self.var_atten_date.get()
                attendance_status = self.var_atten_attendance.get()
                lesson_id = self.var_atten_lesson.get()

                # 连接到 MongoDB
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                db = client["Face_Recognizer"]
                attendance_collection = db["attendance"]

                # 使用 update_one 更新单个文档
                result = attendance_collection.update_one(
                    {"IdAuttendance": atten_id},
                    {
                        "$set": {
                            "Student_id": student_id,
                            "Name": name,
                            "Class": class_name,
                            "Time_in": time_in,
                            "Time_out": time_out,
                            "Date": date,
                            "AttendanceStatus": attendance_status,
                            "Lesson_id": lesson_id,
                        }
                    }
                )

                # 检查是否更新成功
                if result.matched_count > 0:
                    messagebox.showinfo("Success", "Attendance information updated successfully", parent=self.root)
                    self.reset_data()
                    self.fetch_data()
                    client.close()


                else:
                    messagebox.showwarning("Update", "Record not found", parent=self.root)


            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # Delete Function
    def delete_data(self):#hàm xóa dữ liệu
            if self.var_atten_id.get() == "":#nếu bỏ trống id điểm danh
                messagebox.showerror("Error", "ID cannot be left blank ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Delete record", "Do you want to delete this record?", parent=self.root)
                    if delete:
                        client = pymongo.MongoClient(
                            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                        db = client["Face_Recognizer"]
                        attendance_collection = db["attendance"]
                        # 获取要删除的记录的 IdAuttendance
                        atten_id = self.var_atten_id.get()

                        # 使用 delete_one 删除单个文档
                        result = attendance_collection.delete_one({"IdAuttendance": atten_id})


                        # 检查是否删除成功
                        if result.deleted_count > 0:
                            messagebox.showinfo("Delete", "Record deleted successfully", parent=self.root)


                        else:
                            messagebox.showwarning("Delete", "Record not found", parent=self.root)

                        self.reset_data()
                        self.fetch_data()
                        client.close()




                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def openImage(self):  # hàm mở ảnh đã điểm danh
        if self.var_atten_id == "":
            messagebox.showerror("Error", "Please select an ID to view the image", parent=self.root)


        elif (self.var_atten_timein.get() == 'None'):  # nếu ko điểm danh vào
            if not os.path.exists("Check out\ " + str(self.var_atten_id.get()) + ".jpg"):  # nếu ko có ảnh điểm danh ra:
                messagebox.showerror("Error", "No attendance image found", parent=self.root)
            else:  # nếu có ảnh điểm danh ra : hiển thị ảnh điểm danh ra
                img = cv2.imread("Check out\ " + str(self.var_atten_id.get()) + ".jpg")
                img = cv2.resize(img, (300, 300))
                cv2.imshow("Out of Class", img)  # hiển thị ảnh

        elif (self.var_atten_timeout.get() == 'None'):  # nếu ko điểm danh ra
            if not os.path.exists(
                    "Check in\ " + str(self.var_atten_id.get()) + ".jpg"):  # nếu khong có ảnh điểm danh vào
                messagebox.showerror("Error", "No attendance image found", parent=self.root)
            else:  # nếu có ảnh điểm danh vào: hiển thị ảnh điểm danh vào
                img1 = cv2.imread("Check in\ " + str(self.var_atten_id.get()) + ".jpg")
                img1 = cv2.resize(img1, (300, 300))
                cv2.imshow("Into Class", img1)
        elif (
                self.var_atten_timein.get() != 'None' and self.var_atten_timeout.get() != 'None'):  # nếu có cả ảnh điểm danh ra và vào
            img = cv2.imread("Check out\ " + str(self.var_atten_id.get()) + ".jpg")
            img = cv2.resize(img, (300, 300))
            img1 = cv2.imread("Check in\ " + str(self.var_atten_id.get()) + ".jpg")
            img1 = cv2.resize(img1, (300, 300))
            Hori = np.concatenate((img, img1), axis=1)  # ghép 2 ảnh
            cv2.imshow("InAndOutClass", Hori)  # hiển thị ảnh
        else:
            messagebox.showerror("Error", "Attendance photo not found", parent=self.root)

    def search_data(self):#hàm tìm kiếm điểm danh
        if self.var_com_search.get()=="" or self.var_search.get()=="":#nếu ko nhập đủ thông tin tìm kiếm
            messagebox.showerror("Error!","Please provide all required information")

        else:#nếu nhập đủ 
            try:
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                db = client["Face_Recognizer"]
                attendance_collection = db["attendance"]

                if(self.var_com_search.get()=="Attendance ID"):#loại điểm danh là ID Điểm danh thì chuyển về IdAuttendance để truy vấn trong database
                    self.var_com_search.set("IdAuttendance")
                elif(self.var_com_search.get()=="Date"):
                    self.var_com_search.set("Date")
                else:
                    if(self.var_com_search.get()=="Student ID"):
                        self.var_com_search.set("Student ID")
                    elif(self.var_com_search.get()=="Lesson Session ID"):
                        self.var_com_search.set("Lesson_id")

                mydata.clear()#xóa dữ liệu trong mảng data

                search_condition = {str(self.var_com_search.get()): {"$regex": str(self.var_search.get())}}

                # 查詢並取得結果
                data = attendance_collection.find(search_condition, {"_id": 0})
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
                        document["AttendanceStatus"]

                    )
                    insert_data.append(class_data)

                print(insert_data)


                if(len(insert_data) > -1):#nếu có data

                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    for i in insert_data:
                        self.AttendanceReportTable.insert("",END,values=i)
                        mydata.append(i)
                    messagebox.showinfo("Notification","Yes "+str(len(insert_data))+" record that meet the conditions",parent=self.root)

                else:
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    messagebox.showinfo("Notification", "No records meet the requirements",parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
    def today_data(self):#hàm lấy dữ liệu trong ngày
        try:
            client = pymongo.MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            attendance_collection = db["attendance"]

            # Clear data in mydata
            mydata.clear()

            # Get today's date
            d1 = strftime("%d/%m/%Y")

            # Retrieve data from MongoDB based on the Date column
            data = attendance_collection.find({"Date": {"$regex": d1}}, {"_id": 0})

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
                    document["AttendanceStatus"]

                )
                insert_data.append(class_data)

            print(insert_data)


            if (len(insert_data) != 0):#nếu có dữ liệu

                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())#xóa tất cả các dữ liệu cũ trong bảng
                for i in insert_data:#với mỗi dòng trong dữ liệu
                    self.AttendanceReportTable.insert("", END, values=i)# thêm dữ liệu lên bảng
                    mydata.append(i)#truyền dữ liệu vào mảng mydata để xuất excel
                messagebox.showinfo("Notification", "Yes " + str(len(insert_data)) + " today's records",parent=self.root)

            else:#nếu ko có dữ liệu
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())#xóa tất cả dữ liệu trong bảng
                messagebox.showinfo("Notification", "No records exist for today!",parent=self.root)#thông báo
            client.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Attendance(root)#khởi tại object root
    root.mainloop()# cua so hien len