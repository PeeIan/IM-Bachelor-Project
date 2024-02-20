from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
import PIL.ImageOps
from tkinter import messagebox
import mysql.connector
import cv2
from datetime import datetime, date
from time import strftime
from database_str import Database_str
import pymongo
from pymongo import MongoClient

value_from_home = None #從main_upd.py表單傳遞過來的教師ID
def new_tcid(value):#當登入到main_upd.py表單時，獲取教師ID的函數
    global value_from_home
    value_from_home = value



class Face_Recognition:
    # panel=None
    # camara=cv2.VideoCapture(0)
    # btnOpen=None
    # btnClose = None
    #
    # check=1
    # camara.set(3, 800) ##chiều dài
    # camara.set(4, 580)  ##chiều rộng
    # camara.set(10, 150)
    def __init__(self,root):
        w = 1350  # 界面的寬度
        h = 700  # 界面的高度
        self.root = root
        ws = self.root.winfo_screenwidth()  # 屏幕的寬度
        hs = self.root.winfo_screenheight()  # 屏幕的高度
        x = (ws / 2) - (w / 2)  # 距離左邊邊界的位置為 x 像素
        y = (hs / 2) - (h / 2)  # 距離上邊邊界的位置為 y 像素

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))  #界面的尺寸和位置
        self.root.title("Check In System")  #标题
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  #界面图标
        self.isClicked=False  #將isClicked變數設為false以打開/關閉相機，當相機打開時isClicked設為true"。
        self.teacherid = None #教师ID变量

        img3 = PIL.Image.open(r"ImageFaceDetect\bg1.png")#背景图片
        img3 = img3.resize((1350, 700), PIL.Image.ANTIALIAS)#RESIZE
        self.photoimg3 = ImageTk.PhotoImage(img3)

        #数据库连接信息
        self.db = Database_str()


        bg_img = Label(self.root, image=self.photoimg3)#背景标签
        bg_img.place(x=0, y=0, width=1350, height=700)#标签的位置和尺寸

        heading = Label(bg_img, text="Students Check in System", font=("yu gothic ui", 20, "bold"), bg="white",
                        fg="red2",
                        bd=0, relief=FLAT)#红色标题
        heading.place(x=400, y=15, width=550, height=30)

        self.current_image = None


        #teacher _ ID
        print(value_from_home)
        self.teacher_id=value_from_home #选择教师ID = 登录系统的ID
        #lesson_id
        self.lessonid=None#课程ID变量
        #self
        self.className=None

        today = strftime("%d/%m/%Y")#time_today
        subject_array = [] #用于存储课程和课时信息的数组
        #提取当天课程信息
        if(value_from_home=="0" or value_from_home==None):#登录管理员（如果 value_from_home = 0 或 none，则视为使用管理员权限登录）
        	#连接数据库
            # 建立MongoDB連線
            client = MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            lesson_collection = db['lesson']
            self.teacher_id = 0  # 选择教师ID = 0（0用于管理员）
            data = lesson_collection.find(
                {"Date": today},
                {"Class": 1, "Lesson_id": 1, "_id": 0}
            )
            insert_data = []  # 用來存放擷取到的資料
            for document in data:
                # 將每個文件的資料轉換成元組並添加到data中
                class_data = (
                    document["Class"],
                    document["Lesson_id"]

                )
                insert_data.append(class_data)

            print(insert_data)
            for i in insert_data:
                print(i)
                t = str(i).replace("'", "", 4).replace("(", "").replace(")", "").replace(" ",
                                                                                         "") #去除多余字符以显示课程和课时名称
                # print(t)
                subject_array.append(t)#将刚查询到的数据行传递到数组中
        else:#如果使用教师帐户登录
            client = MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            lesson_collection = db['lesson']

            data = lesson_collection.find(
                {"Date": today},
                {"Class": 1, "Lesson_Id": 1, "_id": 0}
            )
            insert_data = []  # 用來存放擷取到的資料
            for document in data:
                # 將每個文件的資料轉換成元組並添加到data中
                class_data = (
                    document["Class"],
                    document["Name"],

                )
                insert_data.append(class_data)

            print(insert_data)


            for i in insert_data:
                t = str(i).replace("'", "", 4).replace("(", "").replace(")", "").replace(" ", "")
                # print(t)
                subject_array.append(t)

        #=======================================LEFT FRAME=========================================
        #包含识别屏幕的框架，包括摄像头和打开、关闭摄像头的按钮
        Left_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Recognition Screen",
                                font=("times new roman", 11, "bold"))#创建框架（self.root在应用程序界面中，bd=2表示2像素的边框）
        Left_frame.place(x=30, y=70, width=780, height=540)#框架的位置

        self.panel = ttk.Label(Left_frame,borderwidth=2, relief="groove")

        self.panel.place(x=8, y=50, width=760, height=420)

        #选择要点名的上课时段
        self.choose_frame = LabelFrame(Left_frame, bd=1, bg="white", relief=RIDGE,
                                  font=("times new roman", 11, "bold"))
        self.choose_frame.place(x=8, y=0, width=760, height=40)

        #选择上课时间
        search_label = Label(self.choose_frame, text="Choose Lesson: ", font=("times new roman", 11, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)


        self.selectsub=StringVar()
        self.lesson_combo = ttk.Combobox(self.choose_frame,textvariable=self.selectsub ,font=("times new roman", 12, "italic"), state="readonly",
                                    width=18)
        self.lesson_combo["values"] = subject_array#Combobox里的值是传递的subject_array数组中的值
        self.lesson_combo.current()#Combobox的初始值为空。
        self.lesson_combo.bind("<<ComboboxSelected>>", self.callbackFunc)
        self.lesson_combo.grid(row=0, column=1, padx=5, pady=10, sticky=W)

        #choose attendance_value
        choose_type_att=Label(self.choose_frame, text="Choose type: ", font=("times new roman", 12, "bold"),
                             bg="white")
        choose_type_att.grid(row=0, column=2, padx=35, pady=10, sticky=W)

        self.type_attendance=StringVar()#考勤类型
        self.type_combo=ttk.Combobox(self.choose_frame,textvariable=self.type_attendance ,font=("times new roman", 11, "bold"), state="readonly",
                                    width=18)
        self.type_combo["values"] = ("In","Out")
        self.type_combo.current(0)
        self.type_combo.grid(row=0, column=3, padx=0, pady=10, sticky=W)


        #考勤通知
        self.notify_frame = LabelFrame(Left_frame, bd=1, bg="white", relief=RIDGE,
                                       font=("times new roman", 11, "bold"))
        self.notify_frame.place(x=8, y=480, width=760, height=35)
        self.notify_label = Label(self.notify_frame, text="Notification: Please choose a lesson to open the camera!!!", font=("times new roman", 11, "bold"),
                             bg="white",fg="red")
        self.notify_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        #相机按钮
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnOpen.png")#相机开启按钮图像
        img_btn1 = img_btn1.resize((350, 45), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        self.btnOpen= Button(self.root ,bg="white", cursor="hand2",
                      borderwidth=0,image=self.photobtn1,command=self.face_recog,fg="white",disabledforeground="black")
        self.btnOpen.place(x=30, y=620, width=350, height=45)
        if self.selectsub.get()=="":#如果未选择课程或上课时间，则不允许开启相机
            self.btnOpen['state'] = "disabled"

        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnClose.png")#相机关闭按钮图像
        img_btn2 = img_btn2.resize((350, 45), PIL.Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        self.btnClose = Button(self.root, cursor="hand2",
                      borderwidth=0,image=self.photobtn2, bg="white",command=self.is_clicked, fg="white")
        self.btnClose.place(x=460, y=620, width=350, height=45)


        #Right_frame

        #包含考勤状态的框架，包括考勤照片、考勤时间和学生姓名等信息
        self.Right_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Check in information",
                                font=("times new roman", 12, "bold"))
        self.Right_frame.place(x=900, y=70, width=400, height=380)

        self.img_right = PIL.Image.open(r"ImageFaceDetect\unknow.jpg")#无人考勤时的默认考勤照片
        self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
        self.photoimg_left = ImageTk.PhotoImage(self.img_right)

        #包含图像的标签
        self.f_lbl = Label(self.Right_frame, image=self.photoimg_left,bg="white",borderwidth=2, relief="groove",highlightcolor="darkblue")
        self.f_lbl.place(x=110, y=10, width=190, height=190)

        self.studentID_atten_info=Label(self.Right_frame, bg="white",
                                font=("times new roman", 12, "bold"))
        self.studentID_atten_info.place(x=5, y=220, width=380, height=120)

        #学生ID
        self.studentID_label = Label(self.studentID_atten_info, text="Student ID: ", font=("times new roman", 11, "bold"), bg="white")
        self.studentID_label.grid(row=0, column=0, padx=10,pady=7, sticky=W)

        self.studentID_atten_label = Label(self.studentID_atten_info, text="", font=("times new roman", 11, "bold"),
                                bg="white")
        self.studentID_atten_label.grid(row=0, column=1, padx=10, pady=7, sticky=W)


        #學生姓名
        self.studentname_label = Label(self.studentID_atten_info, text="Student Name: ", font=("times new roman", 11, "bold"),
                                     bg="white")
        self.studentname_label.grid(row=1, column=0, padx=10, pady=7, sticky=W)

        self.studentname_atten_label = Label(self.studentID_atten_info, text="", font=("times new roman", 11, "bold"),
                                           bg="white")
        self.studentname_atten_label.grid(row=1, column=1, padx=10, pady=7, sticky=W)


        #考勤时间
        self.studentclass_label = Label(self.studentID_atten_info, text="Time: ",
                                       font=("times new roman", 11, "bold"),
                                       bg="white")
        self.studentclass_label.grid(row=2, column=0, padx=10, pady=7, sticky=W)

        self.studentclass_atten_label = Label(self.studentID_atten_info, text="",
                                             font=("times new roman", 11, "bold"),
                                             bg="white")
        self.studentclass_atten_label.grid(row=2, column=1, padx=10, pady=7, sticky=W)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #======================Class-info==============================
        #包含课程信息的框架
        self.RightU_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Lesson Information",
                                      font=("times new roman", 11, "bold"))
        self.RightU_frame.place(x=900, y=465, width=400, height=180)

        #班級
        self.className_label = Label(self.RightU_frame, text="Class: ",
                                     font=("times new roman", 11, "bold"), bg="white")
        self.className_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.className_atten_label = Label(self.RightU_frame, text="", font=("times new roman", 11, "bold"),
                                           bg="white",fg="red2")
        self.className_atten_label.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        #课程/科目
        self.subject_lesson_label = Label(self.RightU_frame, text="Lesson ID: ",
                                       font=("times new roman", 11, "bold"),
                                       bg="white")
        self.subject_lesson_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.subject_lesson_atten_label = Label(self.RightU_frame, text="", font=("times new roman", 11, "bold"),
                                             bg="white",fg="red2")
        self.subject_lesson_atten_label.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        #时间
        self.classtime_label = Label(self.RightU_frame, text="Time: ",
                                        font=("times new roman", 11, "bold"),
                                        bg="white")
        self.classtime_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        self.classtime_atten_label = Label(self.RightU_frame, text="",
                                              font=("times new roman", 11, "bold"),
                                              bg="white",fg="red2")
        self.classtime_atten_label.grid(row=2, column=1, padx=10, pady=10, sticky=W)



        #=============检查今天是否有课程需要考勤=====
        if not subject_array:#如果没有
            self.lesson_combo['state'] = "disabled"#下拉框无法选择
            self.notify_label[
                'text'] = "You have no lesson today."#今天没有课程通知
            self.btnOpen['state']= "disabled"#相机按钮不起作用

    def is_clicked(self):#如果还没有按下相机按钮
        self.isClicked=True
        self.lesson_combo['state'] = "readonly"
        self.type_combo['state']="readonly"
        self.notify_label[
            'text'] = "Please choose a lesson to check in."
        self.notify_label['fg']="red"

        print("Camera is Closed")

    def on_closing(self):#关闭摄像头
        self.isClicked = True
        self.root.destroy()

    def callbackFunc(self,event):#显示课程信息
        mls = event.widget.get()
        # print(mls)

        if self.selectsub.get()=="":#如果不选择课程时间
            self.btnOpen['state'] = "disabled" #相机开关失效
        else:
            c = str(mls).split(",")
            self.className = str(c[0])
            self.lessonid = str(c[1])#课程ID信息
            # self.subject_name=str(c[0]) #课程名称
            # print(self.subject_name)
            self.btnOpen['state']="normal"
            client = MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            lesson_collection = db['lesson']
            get_info = lesson_collection.find_one({"Lesson_id": int(self.lessonid)},
                                           {"Time_start": 1, "Time_end": 1, "Course": 1, "_id": 0})
            timeclass = f"{get_info['Time_start']} - {get_info['Time_end']}"
            class_name = get_info['Course']
            subles=self.lessonid
            self.className_atten_label['text']= get_info['Course']
            self.subject_lesson_atten_label['text']=self.lessonid
            self.classtime_atten_label['text']=timeclass
        # print(self.lessonid)


    #===========attendance===================
    def mark_attendance(self, i, r, n, d, face_cropped):  # 這是一個點名的函數，接受四個參數：i代表學生的ID，r代表身份證號碼，n代表學生的名字，d代表課程（或班級），face_cropped是已經裁剪好的學生臉部的圖像。
        img_id = 0
        self.lesson_combo['state'] = "disabled"  # 這可能是因為在進行點名過程中，ComboBox元件被鎖定或禁用了。
        self.type_combo['state'] = "disabled"
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        attendance_collection = db['attendance']
        lesson_collection = db['lesson']
        student_collection = db['student']
        while True:  # khi camera mở lên không có lỗi
            # Them data len csdl
            now = datetime.now()
            d1 = strftime("%d/%m/%Y")  # ngày hôm nay
            dtString = now.strftime("%H:%M:%S")  # thời điểm hiện tại giờ:phút:giây
            ma = "SV" + str(i) + d1 + self.lessonid  # mã điểm danh =SV+str(i)+ngày hôm nay+id buổi học ()
            masp = ma.replace("/", "")
            # print(masp)
            img_id += 1


            chkStudent = student_collection.find(
                {"Course": self.className},
                {"Student ID": 1, "_id": 0}
            )
            insert_data = []  # 用來存放擷取到的資料
            for document in chkStudent:
                # 將每個文件的資料轉換成元組並添加到data中
                class_data = (
                    document["Student ID"]

                )
                insert_data.append(class_data)

            print(insert_data)

            chkarray = []  # mảng chứa thông tin id học sinh trong lớp học
            for cks in insert_data:
                chkarray.append(cks)

            i = int(i)

            if (i not in chkarray):
                self.notify_label['text'] = "Information: Student " + n + " not in the list."
                print("Student:" + n + " not in the class roster.")
            else:  # nếu học sinh có trong lớp học
                try:
                    i = int(i)


                    insert_data = attendance_collection.find(
                        {"Student_id": i},
                        {"Date": 1, "Lesson_id": 1, "_id": 0}
                    )
                    """
                    insert_data = []  # 用來存放擷取到的資料
                    for document in idn:
                        # 將每個文件的資料轉換成元組並添加到data中
                        class_data = (
                            document["Date"],
                            document["Lesson_id"]

                        )
                        insert_data.append(class_data)

                    print(insert_data)
                    """

                    a = []  # date array
                    b = []  # lesson_id array

                    for i1 in insert_data:
                        a.append(i1["Date"])  # check-in date
                        b.append(i1["Lesson_id"])  # attendance session
                    # nếu chọn loại điểm danh là ra hoặc vào
                    if (self.type_attendance.get() == "In"):
                        if ((d1 not in a)) or ((int(self.lessonid) not in b)):  # 如果今天学生没有点名或学生没有在上课时点名，可以选择


                            # 插入文檔
                            attendance_collection.insert_one({
                                "IdAuttendance": masp,
                                "Student_id": int(i),
                                "Name": n,
                                "class": d,
                                "Time_in": dtString,
                                "Time_out": None,  # 這裡的 field_name_6 需要根據實際情況替換
                                "Date": d1,
                                "Lesson_id": int(self.lessonid),
                                "AttendanceStatus": "",  # 這裡的 field_name_9 需要根據實際情況替換
                            })
                            # 将考勤照片保存到文件夹
                            cv2.imwrite("Check in\ " + masp + ".jpg",
                                        face_cropped)
                            # =============================Check_attendance===============================
                            # Display attendance photo successfully.
                            self.img_right = PIL.Image.open(r"Check in\ " + masp + ".jpg")
                            self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
                            self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                            self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white", borderwidth=1,
                                               relief="groove")
                            self.f_lbl.place(x=110, y=10, width=190, height=190)

                            # id học sinh
                            self.studentID_label = Label(self.studentID_atten_info, text="Student ID:",
                                                         font=("times new roman", 11, "bold"), bg="white")
                            self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                            self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                               font=("times new roman", 11, "bold"),
                                                               bg="white", relief="sunken", width=20, justify="left")
                            self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                            # tên học sinh
                            self.studentname_label = Label(self.studentID_atten_info, text="Student name:",
                                                           font=("times new roman", 11, "bold"),
                                                           bg="white")
                            self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                            self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                 font=("times new roman", 11, "bold"), relief="sunken",
                                                                 width=18,
                                                                 bg="white", justify="left")
                            self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                            # lớp học
                            self.studentclass_label = Label(self.studentID_atten_info, text="Time:",
                                                            font=("times new roman", 11, "bold"),
                                                            bg="white")
                            self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                            self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                  font=("times new roman", 11, "bold"),
                                                                  bg="white", relief="sunken", width=20, justify="left")
                            self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                        else:  # 如果已经点名了
                            # print("Sinh vien:" + n+ " Đã điểm danh ngày "+d1+ ". Vui lòng ra khỏi Camera !!")
                            self.notify_label[
                                'text'] = "Information: Student: " + n + " successfully checked in to class today. "
                            self.notify_label['fg'] = "green"

                            # =====================Change_AttendanceStatus===================================
                            # kiểm tra thời gian vào
                            ckTime_in = attendance_collection.find_one(
                                {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                {"Time_in": 1, "_id": 0}
                            )

                            time_in = ckTime_in["Time_in"]

                            # print(time_in)

                            # -======Timestart========
                            # lấy ra thời gian bắt đầu buổi học
                            ckStart_in = lesson_collection.find_one(
                                {"Lesson_id": int(self.lessonid)},
                                {"Time_start": 1, "_id": 0}
                            )
                            time_start = ckStart_in["Time_start"]

                            time_in = datetime.strptime(time_in, '%H:%M:%S')
                            time_start = datetime.strptime(time_start, '%H:%M:%S')
                            # print(time_start)
                            if (time_in < time_start):  # nếu thời gian điểm danh vào nhỏ hơn thời gian bắt đầu ->Cập nhật trangh thái thành có mặt
                                attendance_collection.update_one(
                                    {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                    {"$set": {"AttendanceStatus": "Present"}}
                                )
                            else:
                                a = datetime.strptime(str(time_in - time_start), '%H:%M:%S').time()#thời gian học sinh điểm danh muộn hơn so với thời gia bắt đầu

                                b = datetime.strptime('0:00:00',
                                                      '%H:%M:%S').time()  # thoi gian dc phep diem danh co mat 15 phut
                                c = datetime.strptime('0:50:00', '%H:%M:%S').time()  # thoi gian dc phep diem danh muon
                                d = datetime.strptime('1:00:00', '%H:%M:%S').time()  # thoi gian cho phep sv vang 1 tiet

                                if (
                                        b < a < c):  # nếu thời gian đi muộn lớn hơn 15 phút và nhỏ hơn 50phuts thì cập nhật trạng thái đi muộn

                                    stt = "Late " + str(a.minute) + " minute(s)"
                                    # print(stt)
                                    attendance_collection.update_one(
                                        {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                        {"$set": {"AttendanceStatus": stt}}
                                    )
                                elif (c < a < d):  # nếu thời gian đi muộn lớn hơn 50 và nhỏ hơn 1 tiếng -> vắng 1 tiết
                                    attendance_collection.update_one(
                                        {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                        {"$set": {"AttendanceStatus": "Absent for one period"}}
                                    )
                                else:  # nếu thời gian đi muộn lớn hơn 1 tiếng -> Vắng
                                    attendance_collection.update_one(
                                        {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                        {"$set": {"AttendanceStatus": "Absent"}}
                                    )
                                # print("Vắng")

                        # self.fetch_data()

                        # messagebox.showinfo("Thành công", "Thêm thông tin Học sinh thành công", parent=self.root)
                    elif (self.type_attendance.get() == "Out"):  # Loại điểm danh ra khỏi lớp : tương tự điểm dah vào


                        # 查詢 MongoDB 以獲取 IdAuttendance
                        data = attendance_collection.find({}, {"IdAuttendance": 1, "_id": 0})

                        insert_data = []  # 用來存放擷取到的資料
                        for document in data:
                            # 將每個文件的資料轉換成元組並添加到data中
                            class_data = (
                                document["IdAuttendance"]

                            )
                            insert_data.append(class_data)

                        print(insert_data)
                        # 將游標結果轉換為列表


                        att = []
                        for ida in insert_data:
                            att.append(ida)
                        if (masp not in att):
                            if ((d1 not in a)) or ((self.lessonid not in b)):

                                attendance_collection.insert_one({
                                    "IdAuttendance": masp,
                                    "Student_id": int(i),
                                    "Name": n,
                                    "class": d,
                                    "Time_in": dtString,
                                    "Time_out": None,  # 這裡的 field_name_6 需要根據實際情況替換
                                    "Date": d1,
                                    "Lesson_id": int(self.lessonid),
                                    "AttendanceStatus": "In attendance",  # 這裡的 field_name_9 需要根據實際情況替換
                                })
                                cv2.imwrite("Check out\ " + masp + ".jpg",
                                        face_cropped)
                                # =============================Check_attendance===============================

                                self.img_right = PIL.Image.open(r"Check out\ " + masp + ".jpg")
                                self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
                                self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white",
                                                   borderwidth=1,
                                                   relief="groove")
                                self.f_lbl.place(x=110, y=10, width=190, height=190)

                                # stdID
                                self.studentID_label = Label(self.studentID_atten_info, text="ID Học sinh:",
                                                             font=("times new roman", 11, "bold"), bg="white")
                                self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                   font=("times new roman", 11, "bold"),
                                                                   bg="white", relief="sunken", width=20,
                                                                   justify="left")
                                self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                # name
                                self.studentname_label = Label(self.studentID_atten_info, text="Tên Học sinh:",
                                                               font=("times new roman", 11, "bold"),
                                                               bg="white")
                                self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                     font=("times new roman", 11, "bold"),
                                                                     relief="sunken",
                                                                     width=18,
                                                                     bg="white", justify="left")
                                self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                # class
                                self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                font=("times new roman", 11, "bold"),
                                                                bg="white")
                                self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                      font=("times new roman", 11, "bold"),
                                                                      bg="white", relief="sunken", width=20,
                                                                      justify="left")
                                self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                            else:
                                # print(
                                #     "Sinh vien:" + n + " Đã điểm danh ngày " + d1 + ". Vui lòng ra khỏi Camera !!")
                                self.notify_label[
                                    'text'] = "Information: Student " + n + " successfully checked out of the course "
                                self.notify_label['fg'] = "green"

                                # =====================Change_AttendanceStatus===================================
                                ckTime_out = attendance_collection.find_one(
                                    {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                    {"Time_out": 1, "_id": 0}
                                )
                                time_out = ckTime_out["Time_out"]
                                # print(time_out)

                                # -======Timeend========

                                ckend_in = lesson_collection.find_one(
                                    {"Lesson_id": int(self.lessonid)},
                                    {"Time_end": 1, "_id": 0}
                                )
                                time_end = ckend_in["Time_end"]

                                # print(time_start)
                                if (time_end < time_out):
                                    attendance_collection.update_one(
                                        {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                        {"$set": {"AttendanceStatus": "Present"}}
                                    )
                                else:
                                    a = datetime.strptime(str(time_end - time_out), '%H:%M:%S').time()
                                    b = datetime.strptime('0:15:00',
                                                          '%H:%M:%S').time()  # thoi gian dc phep diem danh co mat trc 15p
                                    c = datetime.strptime('0:50:00',
                                                          '%H:%M:%S').time()  # thoi gian dc phep diem danh muon

                                    if (a < b):
                                        attendance_collection.update_one(
                                            {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                            {"$set": {"AttendanceStatus": "Present"}}
                                        )
                                    elif (b < a < c):
                                        attendance_collection.update_one(
                                            {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                            {"$set": {"AttendanceStatus": "Missed one period"}}
                                        )

                                    else:
                                        attendance_collection.update_one(
                                            {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                            {"$set": {"AttendanceStatus": "Absent"}}
                                        )


                        else:
                            timeout_check = attendance_collection.find_one(
                                {"IdAuttendance": masp},
                                {"Time_out": 1, "_id": 0}
                            )

                            # 提取 Time_out 的值，如果文档存在
                            timeout_check = timeout_check["Time_out"]
                            if (timeout_check == None):
                                attendance_collection.update_one(
                                    {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                    {"$set": {"Time_out": dtString}}
                                )
                                cv2.imwrite("Check out\ " + masp + ".jpg",
                                        face_cropped)
                                # =============================Check_attendance===============================

                                self.img_right = PIL.Image.open(r"Check out\ " + masp + ".jpg")
                                self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
                                self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white",
                                                   borderwidth=1,
                                                   relief="groove")
                                self.f_lbl.place(x=110, y=10, width=190, height=190)

                                # stdID
                                self.studentID_label = Label(self.studentID_atten_info, text="ID Học sinh:",
                                                             font=("times new roman", 11, "bold"), bg="white")
                                self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                   font=("times new roman", 11, "bold"),
                                                                   bg="white", relief="sunken", width=20,
                                                                   justify="left")
                                self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                # name
                                self.studentname_label = Label(self.studentID_atten_info, text="Tên Học sinh:",
                                                               font=("times new roman", 11, "bold"),
                                                               bg="white")
                                self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                     font=("times new roman", 11, "bold"),
                                                                     relief="sunken",
                                                                     width=18,
                                                                     bg="white", justify="left")
                                self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                # class
                                self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                font=("times new roman", 11, "bold"),
                                                                bg="white")
                                self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                      font=("times new roman", 11, "bold"),
                                                                      bg="white", relief="sunken", width=20,
                                                                      justify="left")
                                self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                            else:
                                # print(
                                #     "Sinh vien:" + n + " Đã điểm danh ngày " + d1 + ". Vui lòng ra khỏi Camera !!")
                                self.notify_label[
                                    'text'] = "Information: Students: " + n + " successfully checked out of the course "
                                self.notify_label['fg'] = "green"
                                # =====================Change_AttendanceStatus===================================
                                ckTime_out = attendance_collection.find_one(
                                    {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                    {"Time_out": 1, "_id": 0}
                                )

                                # 提取 Time_out 的值，如果文档存在
                                time_out = ckTime_out["Time_out"]
                                # print(time_out)

                                # -======Timestart========

                                ckend_in = lesson_collection.find_one(
                                    {"Lesson_id": int(self.lessonid)},
                                    {"Time_end": 1, "_id": 0}
                                )

                                time_end = ckend_in["Time_end"]
                                # print(time_start)
                                if (time_end < time_out):
                                    attendance_collection.update_one(
                                        {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                        {"$set": {"AttendanceStatus": "Present"}}
                                    )
                                else:
                                    a = datetime.strptime(str(time_end - time_out), '%H:%M:%S').time()
                                    b = datetime.strptime('0:15:00',
                                                          '%H:%M:%S').time()  # thoi gian dc phep diem danh co mat trc 15p
                                    c = datetime.strptime('0:50:00',
                                                          '%H:%M:%S').time()  # thoi gian dc phep diem danh muon

                                    if (a < b):
                                        attendance_collection.update_one(
                                            {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                            {"$set": {"AttendanceStatus": "Present"}}
                                        )
                                    elif (b < a < c):
                                        attendance_collection.update_one(
                                            {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                            {"$set": {"AttendanceStatus": "Missed one period"}}
                                        )
                                    else:
                                        attendance_collection.update_one(
                                            {"Student_id": int(i), "Lesson_id": int(self.lessonid)},
                                            {"$set": {"AttendanceStatus": "Absent"}}
                                        )





                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
            if img_id == 1:
                break

    def face_recog(self):  # 人脸识别
        self.isClicked = False  # 如果摄像头已打开

        # 初始化模型
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        student_collection = db['student']
        lesson_collection = db['lesson']

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):  # 在图像框架中确定面部
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将照片转换成黑白照片（灰度图）
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)  # 已识别的面孔

            coord = []
            for (x, y, w, h) in features:  # 对于每个已识别的面孔（通过 x、y、w、h 定义为矩形边界框）
                cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 3)  # 在检测到的人脸周围绘制方框
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])  # 在图像框架中，学生ID与已训练的人脸数据相匹配的比例
                confidence = int((100 * (1 - predict / 300)))  # 正确识别的百分比是多少？
                # print(confidence)
                # 剪裁点名照片
                face_cropped = gray_image[y:y + h + 35, x:x + w + 35]  # 根据识别到的人脸确定裁剪位置
                face_cropped = cv2.cvtColor(face_cropped, cv2.COLOR_GRAY2BGR)
                face_cropped = cv2.resize(face_cropped, (190, 190))  # 调整图片大小

                # 连接数据库


                print("id: " + str(id))

                # 學生姓名
                n = student_collection.find_one(
                    {"Student ID": int(id)},
                    {"Student name": 1, "_id": 0}
                )
                # print(n)
                if n and "Student name" in n:
                    n = n["Student name"]

                    if isinstance(n, list):
                        n = " ".join(n)  # 如果 n 是字符串的列表，將它們用空格連接起來
                    else:
                        n = str(n)  # 如果 n 是單個字符串，確保它是字符串

                else:
                    n = "Unknown"

                # 身分證
                r = student_collection.find_one(
                    {"Student ID": int(id)},
                    {"National ID": 1, "_id": 0}
                )
                r = r["National ID"]
                if r:
                    r = "+".join(map(str, r))
                else:
                    r = "Unknown"

                # 课堂
                d = lesson_collection.find_one(
                    {"Lesson_id": int(self.lessonid)},
                    {"Course": 1, "_id": 0}
                )

                if d and "Course" in d:
                    d = d["Course"]

                    if isinstance(d, list):
                        d = " ".join(d)  # 如果 n 是字符串的列表，將它們用空格連接起來
                    else:
                        d = str(d)  # 如果 n 是單個字符串，確保它是字符串

                # 学生ID
                i = student_collection.find_one(
                    {"Student ID": int(id)},
                    {"Student ID": 1, "_id": 0}
                )
                i = str(i["Student ID"])
                # print(i)
                if i:
                    i = "+".join(map(str, i))
                    i = int(i)
                else:
                    i = "Unknown"

                """
                font_path = "D:/Project(English)/DiemDanhHSAPP/Traditional Chinese/static/NotoSansTC-ExtraBold.ttf"
                font = ImageFont.truetype(font_path, 32)
                img_pil = PIL.Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(img_pil)
                """
                cv2.putText(img, f"Confidence: {confidence}%", (x, y - 60), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                            (255, 255, 255), 2)
                if confidence >= 85:  # 如果正确识别率超过85%
                    """
                    draw.text((x,y-30), f"ID:{i}", font=font, fill=(255,255,255))
                    draw.text((x, y - 5), f"Name:{n}", font=font, fill=(255, 255, 255))
                    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                    """
                    cv2.putText(img, f"ID:{i}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255),
                                2)  # 打印学生ID
                    cv2.putText(img, f"Name:{n}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255),
                                2)  # 打印学生姓名

                    # cv2.imwrite("DiemDanhImage\ " + i + "." + n + '.' + d + ".jpg",
                    #            array[0])

                    self.mark_attendance(i, r, n, d, face_cropped)  # 将考勤信息保存到数据库
                else:  # 如果在已训练的模型中找不到人脸，则打印'Unknown
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                coord = [x, y, w, h]
            return coord

        def recognize(img, clf, faceCascade):  # nhận diện khuôn mặt
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")  # 在框架中检测人脸的模型
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")  # 已训练好的人脸检测模型

        self.camara = cv2.VideoCapture(0)  # 打开摄像头：0 表示网络摄像头
        self.camara.set(3, 800)  # 摄像头长度
        self.camara.set(4, 580)  # 摄像头宽度
        self.camara.set(10, 150)  # 亮度
        while True:  # 如果成功打开

            ret, img = self.camara.read()
            img = recognize(img, clf, faceCascade)  # 将识别函数传递到摄像头
            # cv2.imshow("Welcome to face REg",img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将框架中的图像转换为灰度以进行识别
            img = PIL.Image.fromarray(img, mode='RGB')
            img = PIL.ImageTk.PhotoImage(img)  # convert image for tkinter
            self.panel['image'] = img
            # self.panel.update()
            self.panel.update()

            if (self.isClicked == True):  # 如果按关闭摄像头，那么退出摄像头
                break
        self.camara.release()
        cv2.destroyAllWindows()



if __name__=="__main__":
    root=Tk() #初始化窗口并将根部分分配给它
    obj=Face_Recognition(root)
    root.mainloop()#窗口显示