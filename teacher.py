import random
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
from time import strftime
from tkinter import messagebox
import mysql.connector
from database_str import Database_str
import pymongo
from pymongo import MongoClient

mydata=[]
class Teacher:
    def __init__(self,root):
        self.root=root
        w = 1350  # Height
        h = 700  # Width

        ws = self.root.winfo_screenwidth()  # Screen width
        hs = self.root.winfo_screenheight()  # Screen height
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.root.geometry(
            '%dx%d+%d+%d' % (w, h, x, y))  # Interface size w: length, h: width, x: left margin, y: right margin
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # Icon of the interface
        self.root.title("Facial Recognition System")
        today = strftime("%d-%m-%Y")

        #Database connection information
        self.db=Database_str()

        # ================variable===================
        self.var_name = StringVar()
        self.var_id = StringVar()
        self.var_phone = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()


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
        self.txt = "Managing Teacher Information"
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

        label_Update_att = Label(Left_frame, bg="#F0FFF0", fg="#483D8B", text="Teacher information",
                                 font=("times new roman", 18, "bold"))
        label_Update_att.place(x=0, y=1, width=386, height=35)

        left_inside_frame = Frame(Left_frame, bd=1, bg="white")
        left_inside_frame.place(x=0, y=60, width=380, height=500)

        # idgv
        auttendanceID_label = Label(left_inside_frame, text="Teacher ID:",font=("times new roman", 12, "bold"),
                                    bg="white")
        auttendanceID_label.grid(row=0, column=0, padx=20, pady=10, sticky=W)

        auttendanceID_entry = ttk.Entry(left_inside_frame, textvariable=self.var_id,state="disabled",
                                        font=("times new roman", 12, "bold"),width=22)
        auttendanceID_entry.grid(row=0, column=1, padx=20, pady=10, sticky=W)

        # idstudent
        roll_label = Label(left_inside_frame, text="Full name:", font=("times new roman", 12, "bold"),
                           bg="white")
        roll_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)

        roll_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_name,
                               font=("times new roman", 12, "bold"))
        roll_entry.grid(row=1, column=1, padx=20, pady=10, sticky=W)

        # name
        nameLabel = Label(left_inside_frame, text="Phone number:", font=("times new roman", 12, "bold"),
                          bg="white")
        nameLabel.grid(row=2, column=0, padx=20, pady=10, sticky=W)

        nameLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_phone,
                                    font=("times new roman", 12, "bold"))
        nameLabel_entry.grid(row=2, column=1, padx=20, pady=10, sticky=W)

        # email
        classLabel = Label(left_inside_frame, text="Email:", font=("times new roman", 12, "bold"),
                           bg="white")
        classLabel.grid(row=3, column=0, padx=20, pady=10, sticky=W)

        classLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_email,
                                     font=("times new roman", 12, "bold"))
        classLabel_entry.grid(row=3, column=1, padx=20, pady=10, sticky=W)

        # quét
        timeLabel = Label(left_inside_frame, text="Security question:", font=("times new roman", 12, "bold"),
                          bg="white")
        timeLabel.grid(row=4, column=0, padx=20, pady=10, sticky=W)


        timeLabel_entry = ttk.Combobox(left_inside_frame, width=20, textvariable=self.var_securityQ,
                                    font=("times new roman", 12, "bold"),state='read-only')
        timeLabel_entry["values"] = ("Select", "What do you like to eat?", "Your interests", "Digits you like")
        timeLabel_entry.grid(row=4, column=1, padx=20, pady=10, sticky=W)
        timeLabel_entry.current(0)

        # answer
        dateLabel = Label(left_inside_frame, text="The answer:", font=("times new roman", 12, "bold"),
                          bg="white")
        dateLabel.grid(row=5, column=0, padx=20, pady=10, sticky=W)

        dateLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_securityA,
                                    font=("times new roman", 12, "bold"))
        dateLabel_entry.grid(row=5, column=1, padx=20, pady=10, sticky=W)

        # pass
        passLabel = Label(left_inside_frame, text="Password:", font=("times new roman", 12, "bold"),
                                 bg="white")
        passLabel.grid(row=6, column=0, padx=20, pady=5, sticky=W)

        passLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_pass,
                                    font=("times new roman", 12, "bold"))
        passLabel_entry.grid(row=6, column=1, padx=20, pady=5, sticky=W)



        # =====btn_frame============
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn1 = img_btn1.resize((150, 35), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)

        btn_frame = Frame(left_inside_frame, bg="white")
        btn_frame.place(x=0, y=350, width=440, height=115)

        add_btn = Button(btn_frame, text="Add new", command=self.add_data, font=("times new roman", 11, "bold"),
                         bd=0, bg="white", cursor='hand2', activebackground='white',
                         width=150, image=self.photobtn1, fg="white", compound="center")
        add_btn.grid(row=9, column=0, pady=10,padx=15)

        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data,
                            font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        delete_btn.grid(row=9, column=1, pady=10,padx=15)

        update_btn = Button(btn_frame, text="Update", command=self.update_data, font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        update_btn.grid(row=10, column=0, pady=20, padx=15)

        reset_btn = Button(btn_frame, text="Refresh", command=self.reset_data, font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=150, image=self.photobtn1, fg="white", compound="center")
        reset_btn.grid(row=10, column=1, pady=0,padx=15)

        # ==================right_ label========================
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=410, y=5, width=880, height=580)

        # search
        self.var_com_search = StringVar()
        search_label = Label(Right_frame, text="Search by :", font=("times new roman", 11, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=15, pady=5, sticky=W)

        search_combo = ttk.Combobox(Right_frame, font=("times new roman", 11, "bold"), textvariable=self.var_com_search,
                                    state="read only",
                                    width=13)
        search_combo["values"] = ("Teacher ID", "Teacher name", "Phone number")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=15, sticky=W)

        self.var_search = StringVar()
        search_entry = ttk.Entry(Right_frame, textvariable=self.var_search, width=15,
                                 font=("times new roman", 11, "bold"))
        search_entry.grid(row=0, column=2, padx=15, pady=5, sticky=W)

        search_btn = Button(Right_frame, command=self.search_data, text="Search",
                            font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=150,image=self.photobtn1,fg="white",compound="center")
        search_btn.grid(row=0, column=3, padx=15)



        showAll_btn = Button(Right_frame, text="View all", command=self.fetch_data,
                             font=("times new roman", 11, "bold"),bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=150,image=self.photobtn1,fg="white",compound="center")
        showAll_btn.grid(row=0, column=5, padx=15)

        # table_frame
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=55, width=860, height=510)

        # scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(table_frame, column=(
        "id", "name", "phone", "email", "quest", "answer", "pass"),
                                                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id", text="Teacher ID")

        self.AttendanceReportTable.heading("name", text="Teacher name")
        self.AttendanceReportTable.heading("phone", text="Phone number")
        self.AttendanceReportTable.heading("email", text="Email")
        self.AttendanceReportTable.heading("quest", text="Security question")
        self.AttendanceReportTable.heading("answer", text="Answer")
        self.AttendanceReportTable.heading("pass", text="Password")


        self.AttendanceReportTable["show"] = "headings"

        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("phone", width=100)
        self.AttendanceReportTable.column("email", width=100)
        self.AttendanceReportTable.column("quest", width=200)
        self.AttendanceReportTable.column("answer", width=200)
        self.AttendanceReportTable.column("pass", width=100)


        self.AttendanceReportTable.pack(fill=BOTH, expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()  # Load data into the grid
        # ================fetchData======================

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
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        teacher_collection = db['teacher']
        lastid = teacher_collection.find_one(
            {},
            {"Teacher_id": 1},
            sort=[("Teacher_id", pymongo.DESCENDING)]
        )
        lastid=lastid["Teacher_id"]
        if (lastid == None):
            self.var_id.set("1")
        else:
            nextid = int(lastid) + 1
            self.var_id.set(str(nextid))

        # return  self.var_id

    def get_cursor(self,event=""):
        cursor_row=self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        self.var_id.set(rows[0])
        self.var_name.set(rows[1])
        self.var_phone.set(rows[2])
        self.var_email.set(rows[3])
        self.var_securityQ.set(rows[4])
        self.var_securityA.set(rows[5])
        self.var_pass.set(rows[6])

    def add_data(self):
        if self.var_securityQ.get()=="Select" or self.var_id.get()=="" or self.var_name.get()=="":
            messagebox.showerror("Error","Please enter complete information",parent=self.root)
        else:
            try:
                client = MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                teacher_collection = db['teacher']
                # 假设你的参数值
                teacher_data = {
                    "Teacher_id": self.var_id.get(),
                    "Name": self.var_name.get(),
                    "Phone": self.var_phone.get(),
                    "Email": self.var_email.get(),
                    "SecurityQ": self.var_securityQ.get(),
                    "SecurityA": self.var_securityA.get(),
                    "Password": self.var_pass.get(),
                }

                # 插入 MongoDB 中的 "teacher" 集合
                teacher_collection.insert_one(teacher_data)

                self.fetch_data()
                self.reset_data()
                messagebox.showinfo('Success','Teacher information has been added successfully!',parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    def reset_data(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_phone.set("")
        self.var_email.set("")
        self.var_securityQ.set("")
        self.var_securityA.set("")
        self.var_pass.set("")
        self.getNextid()
    def fetch_data(self):
            # global mydata
            # mydata.clear()
            client = MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            teacher_collection = db['teacher']

            data = teacher_collection.find().sort("Teacher_id", 1)

            insert_data = []  # 用來存放擷取到的資料

            for document in data:
                # 將每個文件的資料轉換成元組並添加到data中
                teacher_data = (
                    document["Teacher_id"],
                    document["Name"],
                    document["Phone"],
                    document["Email"],
                    document["SecurityQ"],
                    document["SecurityA"],
                    document["Password"]

                )
                insert_data.append(teacher_data)

                # 顯示資料到表格上，這部分與原始程式碼相同
            if len(insert_data) != 0:
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                for i in insert_data:
                    self.AttendanceReportTable.insert("", END, values=i)

            client.close()  # 關閉與MongoDB的連接

    def update(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
    def update_data(self):
        if self.var_securityQ.get()=="Select" or self.var_id.get()=="" or self.var_name.get()=="":
            messagebox.showerror("Error","Please enter complete information",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this record?",parent=self.root)
                if Update>0:
                    client = MongoClient(
                        "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                    # 指定資料庫
                    db = client["Face_Recognizer"]
                    teacher_collection = db['teacher']
                    query = {'Teacher_id': self.var_id.get()}
                    update_data = {
                        '$set': {
                            'Name': self.var_name.get(),
                            'Phone': self.var_phone.get(),
                            'Email': self.var_email.get(),
                            'SecurityQ': self.var_securityQ.get(),
                            'SecurityA': self.var_securityA.get(),
                            'Password': self.var_pass.get(),
                        }
                    }

                    teacher_collection.update_one(query, update_data)

                else:
                    if not Update:
                        return
                messagebox.showinfo('Success','Attendance information has been updated successfully.',parent=self.root)

                self.fetch_data()
                self.reset_data()

            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # Delete Function
    def delete_data(self):
            if self.var_id == "":
                messagebox.showerror("Error", "ID cannot be left blank ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Delete record", "Do you want to delete this record?", parent=self.root)
                    if delete > 0:
                        client = MongoClient(
                            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                        # 指定資料庫
                        db = client["Face_Recognizer"]
                        teacher_collection = db['teacher']
                        query = {'Teacher_id': self.var_id.get()}
                        teacher_collection.delete_one(query)
                    else:
                        if not delete:
                            return
                    # self.fetch_data()
                    messagebox.showinfo("Delete", "Record has been deleted successfully.", parent=self.root)
                    self.fetch_data()
                    self.reset_data()
                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def search_data(self):
        if self.var_com_search.get()=="" or self.var_search.get()=="":
            messagebox.showerror("Error!","Please enter complete information.")

        else:
            try:
                client = MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                teacher_collection = db['teacher']

                if(self.var_com_search.get()=="Teacher ID"):
                    self.var_com_search.set("Teacher_id")
                elif(self.var_com_search.get()=="Teacher name"):
                    self.var_com_search.set("Name")
                else:
                    if(self.var_com_search.get()=="Phone number"):
                        self.var_com_search.set("Phone")

                search_column = self.var_com_search.get()
                search_value = {'$regex': '.*' + self.var_search.get() + '.*'}
                query = {search_column: search_value}

                # 执行MongoDB查询
                data = teacher_collection.find(query)
                data = list(data)

                if(len(data)!=0):
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    for i in data:
                        self.AttendanceReportTable.insert("",END,values=i)
                    messagebox.showinfo("Notification","Yes "+str(len(data))+" records match the conditions",parent=self.root)

                else:
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    messagebox.showinfo("Notification", "No records match the conditions",parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() # Initialize the window and assign root
    obj=Teacher(root)
    root.mainloop()# Show window