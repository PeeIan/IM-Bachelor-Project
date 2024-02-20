import random
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
from time import strftime
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from tkcalendar import DateEntry
from database_str import Database_str
import pymongo
from pymongo import MongoClient

mydata=[]
class Lesson:
    def __init__(self,root):
        self.root=root
        w = 1350  # chiều dài
        h = 700  # chiều rộng

        ws = self.root.winfo_screenwidth()  # chiều dài màn hình
        hs = self.root.winfo_screenheight()  # chiều rộng màn hình
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.root.geometry(
            '%dx%d+%d+%d' % (w, h, x, y))  # kích thước giao diện w:chiều dài,h:rộng,x:cách lề trái,y: cách lề phải
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # icon của giao diện
        self.root.title("Facial Recognition System")
        today = strftime("%d-%m-%Y")

        # thông tin kết nối database
        self.db = Database_str()
        
        # ================variable===================

        self.var_id = StringVar()
        self.var_timestart = StringVar()
        self.var_timeend = StringVar()
        self.var_class=StringVar()
        self.var_classname = StringVar()
        # self.var_teacherid = StringVar()
        # self.var_subjectid = StringVar()



        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")
        img3 = img3.resize((1350, 700), PIL.Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1350, height=700)

        #==================================heading====================================
        #====time====
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")
        img_time = img_time.resize((27, 27), PIL.Image.ANTIALIAS)
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime,bg="white")
        time_img.place(x=43, y=40, width=27, height=27)
        def time():
            string=strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000,time)
        lbl=Label(self.root,font=("times new roman", 11, "bold"),bg="white", fg="black")
        lbl.place(x=80,y=35,width=100,height=20)
        time()
        lbl1 = Label(self.root,text=today, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=20)

        #====title=========
        self.txt = "Manage Class Schedule Information"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 22, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=350, y=22, width=600)
        # self.slider()
        # self.heading_color()

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=24, y=90, width=1293, height=586)

        # ===================left_label=====================
        self.getNextid()
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=5, width=390, height=580)

        label_Update_att = Label(Left_frame, bg="#F0FFF0", fg="#483D8B", text="Class Information",
                                 font=("times new roman", 18, "bold"))
        label_Update_att.place(x=0, y=1, width=386, height=35)

        left_inside_frame = Frame(Left_frame, bd=1, bg="white")
        left_inside_frame.place(x=0, y=60, width=380, height=500)

        # lessonid
        auttendanceID_label = Label(left_inside_frame, text="ID of the class session:", font=("times new roman", 11, "bold"),
                                    bg="white")
        auttendanceID_label.grid(row=0, column=0, padx=20, pady=10, sticky=W)

        auttendanceID_entry = ttk.Entry(left_inside_frame, textvariable=self.var_id, state="disabled",
                                        font=("times new roman", 11, "bold"), width=22)
        auttendanceID_entry.grid(row=0, column=1, padx=20, pady=10, sticky=W)

        # timestart
        roll_label = Label(left_inside_frame, text="Start time:", font=("times new roman", 11, "bold"),
                           bg="white")
        roll_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)

        self.timestart_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_timestart,
                               font=("times new roman", 11, "bold"))
        self.timestart_entry.grid(row=1, column=1, padx=20, pady=10, sticky=W)
        self.timestart_entry.insert(END, "")
        self.timestart_entry.bind('<KeyRelease>', self.timestart)

        # timeend
        nameLabel = Label(left_inside_frame, text="End time:", font=("times new roman", 11, "bold"),
                          bg="white")
        nameLabel.grid(row=2, column=0, padx=20, pady=10, sticky=W)

        self.timeend_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_timeend,
                                    font=("times new roman", 11, "bold"))
        self.timeend_entry.grid(row=2, column=1, padx=20, pady=10, sticky=W)
        self.timeend_entry.insert(END, "")
        self.timeend_entry.bind('<KeyRelease>', self.timeend)

        #date

        dob_label = Label(left_inside_frame, text="Day:", font=("times new roman", 12, "bold"),
                          bg="white")
        dob_label.grid(row=3, column=0, padx=20, pady=10, sticky=W)

        self.dob_entry = DateEntry(left_inside_frame, width=20, bd=3, selectmode='day',
                                   year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 12),
                                   day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=3, column=1, padx=20, pady=10, sticky=W)

        # class

        classLabel = Label(left_inside_frame, text="Class:", font=("times new roman", 11, "bold"),
                           bg="white")
        classLabel.grid(row=4, column=0, padx=20, pady=10, sticky=W)

        self.classLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_class,
                                     font=("times new roman", 11, "bold"))
        self.classLabel_entry.grid(row=4, column=1, padx=20, pady=10, sticky=W)

        # class name

        classnameLabel = Label(left_inside_frame, text="Class name:", font=("times new roman", 11, "bold"),
                           bg="white")
        classnameLabel.grid(row=5, column=0, padx=20, pady=10, sticky=W)

        self.classnameLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_classname,
                                     font=("times new roman", 11, "bold"))
        self.classnameLabel_entry.grid(row=5, column=1, padx=20, pady=10, sticky=W)


        # =====btn_frame============
        #ảnh nút đỏ resize
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn1 = img_btn1.resize((150, 35), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        #frame chứa các nút
        btn_frame = Frame(left_inside_frame, bg="white")
        btn_frame.place(x=0, y=300, width=440, height=115)

        add_btn = Button(btn_frame, text="Add new", command=self.add_data, font=("times new roman", 11, "bold"),
                         bd=0, bg="white", cursor='hand2', activebackground='white',
                         width=150, image=self.photobtn1, fg="white", compound="center")
        add_btn.grid(row=9, column=0, pady=10, padx=20)

        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data,
                            font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        delete_btn.grid(row=9, column=1, pady=10, padx=20)

        update_btn = Button(btn_frame, text="Update", command=self.update_data, font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        update_btn.grid(row=10, column=0, pady=20, padx=20)

        reset_btn = Button(btn_frame, text="Refresh", command=self.reset_data, font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=150, image=self.photobtn1, fg="white", compound="center")
        reset_btn.grid(row=10, column=1, pady=0, padx=20)

        # ==================right_ label========================
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=410, y=5, width=880, height=580)

        # search
        self.var_com_search = StringVar()
        search_label = Label(Right_frame, text="Search By :", font=("times new roman", 11, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=15, pady=5, sticky=W)

        search_combo = ttk.Combobox(Right_frame, font=("times new roman", 11, "bold"), textvariable=self.var_com_search,
                                    state="read only",
                                    width=13)
        search_combo["values"] = ("Class Session ID", "Class","Date Of Class")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=15, sticky=W)

        self.var_search = StringVar()
        search_entry = ttk.Entry(Right_frame, textvariable=self.var_search, width=15,
                                 font=("times new roman", 11, "bold"))
        search_entry.grid(row=0, column=2, padx=15, pady=5, sticky=W)

        search_btn = Button(Right_frame, command=self.search_data, text="Search",
                            font=("times new roman", 11, "bold"),  bd=0, bg="white", cursor='hand2', activebackground='white',
                         width=150, image=self.photobtn1, fg="white", compound="center")
        search_btn.grid(row=0, column=3, padx=15)

        showAll_btn = Button(Right_frame, text="View All", command=self.fetch_data,
                             font=("times new roman", 11, "bold"),  bd=0, bg="white", cursor='hand2', activebackground='white',
                         width=150, image=self.photobtn1, fg="white", compound="center")
        showAll_btn.grid(row=0, column=5, padx=15)

        # table_frame
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=55, width=860, height=510)

        # scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(table_frame, column=(
            "id", "timestart", "timeend", "date", "class","course"),
                                                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id", text="Class Session ID")
        self.AttendanceReportTable.heading("timestart", text="Start time")
        self.AttendanceReportTable.heading("timeend", text="End time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("class", text="Class")
        self.AttendanceReportTable.heading("course", text="Course")


        self.AttendanceReportTable["show"] = "headings"

        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("timestart", width=100)
        self.AttendanceReportTable.column("timeend", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("class", width=100)
        self.AttendanceReportTable.column("course", width=100)



        self.AttendanceReportTable.pack(fill=BOTH, expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()  # load du lieu len grid

    #================Function===================
    def timestart(self, event):#Hàm nhập thời gian giờ:phút giây theo định dạng
            if len(self.timestart_entry.get()) is 2:
                self.timestart_entry.insert(END, ":")
            elif len(self.timestart_entry.get()) is 5:
                self.timestart_entry.insert(END, ":")
            elif len(self.timestart_entry.get()) is 9:
                self.timestart_entry.delete(8, END)
    def timeend(self, event):
            if len(self.timeend_entry.get()) is 2:
                self.timeend_entry.insert(END, ":")
            elif len(self.timeend_entry.get()) is 5:
                self.timeend_entry.insert(END, ":")
            elif len(self.timeend_entry.get()) is 9:
                self.timeend_entry.delete(8, END)
    def slider(self):
        if self.count>=len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text+self.txt[self.count]
            self.heading.config(text=self.text)

        self.count+=1

        self.heading.after(100,self.slider)

    def heading_color(self):
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)


    def getNextid(self):
        # 假设你已经建立了 MongoDB 连接和选择了数据库和集合

        client = pymongo.MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        # 指定集合（collection）
        lesson_collection = db["lesson"]

        # 查询 Lesson_id 列的最大值
        lastid = lesson_collection.find_one({}, sort=[("Lesson_id", -1)])
        if lastid is None:
            self.var_id.set("1")
        else:
            nextid = int(lastid["Lesson_id"]) + 1
            self.var_id.set(str(nextid))


    def get_cursor(self,event=""):
        cursor_row=self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        self.var_id.set(rows[0])
        self.var_timestart.set(rows[1])
        self.var_timeend.set(rows[2])
        self.dob_entry.set_date(rows[3])
        self.var_class.set(rows[4])
        self.var_classname.set(rows[5])



    def add_data(self):

        # =========check class============
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

        arrayClass = []
        for chk in insert_data:
            arrayClass.append(str(chk[0]))
        client.close()

        #check_time
        time_start = datetime.strptime(self.var_timestart.get(), '%H:%M:%S').time() #chuyển txt time_start về dạng thời gian để so sánh
        time_end = datetime.strptime(self.var_timeend.get(), '%H:%M:%S').time()

        if self.var_id.get()=="" or self.var_timestart.get()=="" or self.var_timeend.get()=="" \
                or self.dob_entry.get_date().strftime('%d/%m/%Y')=="" or self.var_class.get()=="" or self.var_class.get()=="":
            messagebox.showerror("Error","Please enter complete information.",parent=self.root)


        elif(self.var_class.get() not in arrayClass):
            messagebox.showerror("Error","This class does not exist !!! ",parent=self.root)
        elif(time_end<time_start):
            messagebox.showerror("Error","The end time cannot be earlier than the start time!",parent=self.root)

        else:
            try:
                client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定数据库
                db = client["Face_Recognizer"]
                # 指定集合（collection）
                lesson_collection = db["lesson"]

                # 插入课程信息到 MongoDB
                lesson_data = {
                    "Lesson_id": int(self.var_id.get()),
                    "Time_start": self.var_timestart.get(),
                    "Time_end": self.var_timeend.get(),
                    "Date": self.dob_entry.get_date().strftime('%d/%m/%Y'),
                    "Class": self.var_class.get(),
                    "Course": self.var_classname.get(),
                }

                lesson_collection.insert_one(lesson_data)

                # 在这之后可以进行其他操作，比如调用 fetch_data()、reset_data() 等
                self.fetch_data()
                self.reset_data()
                client.close()

                messagebox.showinfo("Success", "Added class session information successfully.", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    def reset_data(self):
        self.var_id.set("")
        self.var_timestart.set("")
        self.var_timeend.set("")
        self.var_class.set("")
        self.var_classname.set("")
        self.dob_entry.set_date(strftime("%d/%m/%Y"))
        self.getNextid()
    def fetch_data(self):
            # global mydata
            # mydata.clear()
            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            lesson_collection = db["lesson"]

            data = lesson_collection.find({}, {"_id": 0})
            insert_data = []  # 用來存放擷取到的資料
            for document in data:
                # 將每個文件的資料轉換成元組並添加到data中
                class_data = (
                    document["Lesson_id"],
                    document["Time_start"],
                    document["Time_end"],
                    document["Date"],
                    document["Class"],
                    document["Course"]

                )
                insert_data.append(class_data)

            print(insert_data)



            if len(insert_data) != 0:
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                for i in insert_data:
                    self.AttendanceReportTable.insert("", END, values=i)
                    mydata.append(i)

            else:
                for item in self.AttendanceReportTable.get_children():
                    self.AttendanceReportTable.delete(item)
            client.close()
    def update(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
    def update_data(self):
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

        arrayClass = []
        for chk in insert_data:
            arrayClass.append(str(chk[0]))

        client.close()
        # check_time
        time_start = datetime.strptime(self.var_timestart.get(), '%H:%M:%S').time()
        time_end = datetime.strptime(self.var_timeend.get(), '%H:%M:%S').time()

        if self.var_id.get()=="" or self.var_timestart.get()=="" or self.var_timeend.get()=="" \
                or self.dob_entry.get_date().strftime('%d/%m/%Y')=="" or self.var_class.get()=="" or self.var_class.get()=="":
            messagebox.showerror("Error","Please enter complete information.",parent=self.root)
        elif (self.var_class.get() not in arrayClass):
            messagebox.showerror("Error","It looks like you didn't enter all the required information. Please enter all the necessary details! ",parent=self.root)
        elif (time_end < time_start):
            messagebox.showerror("Error", "End time cannot be earlier than start time!", parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this record?",parent=self.root)
                if Update>0:
                    # 连接到 MongoDB
                    client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                    # 指定数据库
                    db = client["Face_Recognizer"]
                    # 指定集合（collection）
                    lesson_collection = db["lesson"]

                    # 更新课程信息
                    lesson_collection.update_one(
                        {"Lesson_id": int(self.var_id.get())},
                        {"$set": {
                            "Time_start": self.var_timestart.get(),
                            "Time_end": self.var_timeend.get(),
                            "Date": self.dob_entry.get_date().strftime('%d/%m/%Y'),
                            "Class": self.var_class.get(),
                            "Course": self.var_classname.get()
                        }}
                    )
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success","Update information of the class session successfully.",parent=self.root)

                self.fetch_data()
                self.reset_data()
                client.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # Delete Function
    def delete_data(self):
            if self.var_id == "":
                messagebox.showerror("Error", "ID cannot be left blank. ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Delete record", "Do you want to delete this record?", parent=self.root)
                    if delete > 0:
                        # 连接到 MongoDB
                        client = MongoClient(
                            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                        # 指定数据库
                        db = client["Face_Recognizer"]
                        # 指定集合（collection）
                        lesson_collection = db["lesson"]

                        # 删除指定 Lesson_id 的课程信息
                        lesson_collection.delete_one({"Lesson_id": int(self.var_id.get())})

                        client.close()
                    else:
                        if not delete:
                            return

                    # self.fetch_data()

                    messagebox.showinfo("Delete", "Record deleted successfully.", parent=self.root)
                    self.fetch_data()
                    self.reset_data()
                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def search_data(self):
        if self.var_com_search.get()=="" or self.var_search.get()=="":
            messagebox.showerror("Error!","Please enter complete information.")

        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Học sinh"
                if(self.var_com_search.get()=="Class"):
                    self.var_com_search.set("Class")
                elif(self.var_com_search.get()=="Class Session ID"):
                    self.var_com_search.set("Lesson_id")
                else:
                    if(self.var_com_search.get()=="Date Of Class"):
                        self.var_com_search.set("Date")
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                # 指定集合（collection）
                lesson_collection = db["lesson"]
                data = lesson_collection.find({}, {"_id": 0})
                insert_data = []  # 用來存放擷取到的資料
                for document in data:
                    # 將每個文件的資料轉換成元組並添加到data中
                    class_data = (
                        document["Class"],
                        document["Name"],

                    )
                    insert_data.append(class_data)

                if len(insert_data)!=0:
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    for i in insert_data:
                        self.AttendanceReportTable.insert("",END,values=i)
                    messagebox.showinfo("Notification", "There are"+str(len(insert_data))+"records satisfy the condition.",parent=self.root)
                    conn.commit()
                else:
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    messagebox.showinfo("Notification", "No records found that meet the criteria.",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Lesson(root)
    root.mainloop()# cua so hien len