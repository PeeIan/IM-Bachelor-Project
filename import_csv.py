from PIL import Image, ImageTk
from tkinter import *
import chardet
import PIL.Image ,PIL.ImageDraw
import csv
from tkinter import filedialog
import os
import mysql.connector
from tkinter import messagebox
import pandas as pd
import pymongo
from pymongo import MongoClient

from database_str import Database_str
mydata=[]
class InsertData:
    def __init__(self,root):
        self.root=root
        self.root.title("Manage Information")#Title
        self.root.geometry("900x550+0+0")
        self.root.config(bg="#021e2f")
        left_lbl = Label(self.root, bg="#08A3D2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=400)
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  #界面的圖示
        right_lbl = Label(self.root, bg="white", bd=2)
        right_lbl.place(x=200, y=0, relheight=1, relwidth=1)

        # ===========Frame===========
        #資料庫連接的信息
        self.db = Database_str()

        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn1 = img_btn1.resize((120, 30), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)


        title = Label(right_lbl, text="Add student list: ", font=("times new roman", 12, "bold"), bg="white",
                      fg="black").place(x=50, y=40)

        #選擇學生名單文件
        btn_choose = Button(right_lbl, text="Choose File...", command=self.insert_stu, font=("times new roman", 11, "normal"),
                           bd=0,image=self.photobtn1,fg="white", compound="center",
                            cursor="hand2").place(x=250, y=40, width=120, height=30)

        title1 = Label(right_lbl, text="Add class schedule: ", font=("times new roman", 12, "bold"), bg="white",
                      fg="black").place(x=50, y=100)

        #選擇課堂名單文件
        btn_choose2  = Button(right_lbl, text="Choose File...", command=self.insert_less,
                           font=("times new roman", 11, "normal"),
                            bd=0,image=self.photobtn1,fg="white", compound="center",
                           bg="#DCDCDC", cursor="hand2").place(x=250, y=100, width=120, height=30)



        #刪除所有學生
        btn_choose4  = Button(right_lbl, text="Delete", command=self.delete_student,
                           font=("times new roman", 11, "normal"),
                           bd=0,image=self.photobtn1,fg="white", compound="center",
                           bg="#DCDCDC", cursor="hand2").place(x=400, y=40, width=120, height=30)

        #刪除所有課堂
        btn_choose5  = Button(right_lbl, text="Delete", command=self.delete_lesson,
                           font=("times new roman", 11, "normal"),
                            bd=0,image=self.photobtn1,fg="white", compound="center",
                           bg="#DCDCDC", cursor="hand2").place(x=400, y=100, width=120, height=30)

        # 匯出學生資料
        btn_export_students = Button(right_lbl, text="Export Students", command=self.export_stu,
                            font=("times new roman", 11, "normal"),
                            bd=0, image=self.photobtn1, fg="white", compound="center",
                            cursor="hand2").place(x=550, y=40, width=120, height=30)

        # 匯出課堂資料
        btn_export_class = Button(right_lbl, text="Export Class", command=self.export_lesson,
                                     font=("times new roman", 11, "normal"),
                                     bd=0, image=self.photobtn1, fg="white", compound="center",
                                     cursor="hand2").place(x=550, y=100, width=120, height=30)







    #以下是將學生清單從CSV文件中導入的程式碼（中文翻譯）
    def insert_stu(self):
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

            df = pd.read_csv(fln, encoding = encoding)  # 讀取選擇的Excel文件

            for index, row in df.iterrows():
                mydata.append({
                    "Student ID": row[0],
                    "Year": row[1],
                    "Campus": row[2],
                    "Student name": row[3],
                    "Course": row[4],
                    "National ID": row[5],
                    "Gender": row[6],
                    "Birthday": row[7],
                    "E-mail": row[8],
                    "Phone number": row[9][1:],
                    "Address": row[10],
                    "Image status": row[11],
                })

            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            student_collection = db["student"]

            # 插入數據到 MongoDB
            student_collection.insert_many(mydata)

            messagebox.showinfo("Notification:", "Added student list successfully!")
            client.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def insert_less(self):
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


            df = pd.read_csv(fln, encoding=encoding)  # 讀取選擇的Excel文件

            for index, row in df.iterrows():
                mydata.append({
                    "Lesson_id": row[0],
                    "Time_start": row[1],
                    "Time_end": row[2],
                    "Date": row[3],
                    "Class": row[4],
                    "Course": row[5]

                })

            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            # 指定集合（collection）
            lesson_collection = db["lesson"]

            # 插入數據到 MongoDB
            lesson_collection.insert_many(mydata)

            messagebox.showinfo("Notification:", "Added lesson list successfully!")
            client.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)



    def delete_student(self):#删除学生的函数
            try:

                delete=messagebox.askyesno("Delete students","Do you want to delete all students?",parent=self.root)
                if delete>0:
                        client = pymongo.MongoClient(
                            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                        # 指定資料庫
                        db = client["Face_Recognizer"]
                        # 指定集合（collection）
                        student_collection = db["student"]
                        # 删除所有学生
                        student_collection.delete_many({})

                        client.close()
                else:
                    if not delete:
                        return

                messagebox.showinfo("Delete","Student deleted successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    def delete_lesson(self):#删除所有课程的函数
            try:
                delete = messagebox.askyesno("Delete students", "Do you want to delete all students?", parent=self.root)
                if delete > 0:
                    client = pymongo.MongoClient(
                        "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                    # 指定資料庫
                    db = client["Face_Recognizer"]
                    # 指定集合（collection）
                    lesson_collection = db["lesson"]
                    # 删除所有学生
                    lesson_collection.delete_many({})

                    client.close()
                else:
                    if not delete:
                        return

                messagebox.showinfo("Delete", "Lesson deleted successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    def export_stu(self):
        try:
            # 连接到 MongoDB
            client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            student_collection = db["student"]

            # 从 MongoDB 中检索学生数据
            cursor = student_collection.find()
            records = list(cursor)

            # 将学生数据写入 CSV 文件
            with open('student_export.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['Student ID', 'Year', 'Campus', 'Student name', 'Course', 'National ID', 'Gender', 'Birthday', 'E-mail', 'Phone number',
                     'Address', 'Image status'])
                for record in records:
                    writer.writerow([
                        record.get("Student ID", ""),
                        record.get("Year", ""),
                        record.get("Campus", ""),
                        record.get("Student name", ""),
                        record.get("Course", ""),
                        record.get("National ID", ""),
                        record.get("Gender", ""),
                        record.get("Birthday", ""),
                        record.get("E-mail", ""),
                        "'" + record.get("Phone number", ""),  # 将电话号码包装在双引号中
                        record.get("Address", ""),
                        record.get("Image status", "")
                    ])

            messagebox.showinfo("Export", "Students information derived successfully！", parent=self.root)
            client.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due to：{str(es)}", parent=self.root)

    def export_lesson(self):#Python語法
        try:#Python語法
            # 连接到 MongoDB
            client = MongoClient("mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            db = client["Face_Recognizer"]
            lesson_collection = db["lesson"]

            # 从 MongoDB 中检索学生数据
            cursor = lesson_collection.find()
            records = list(cursor)



            # 将学生数据写入 CSV 文件
            with open('lesson_export.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                print(["Lesson_id", 'Time_start', 'Time_end', 'Date', 'Class', 'Course'])
                writer.writerow(["Lesson_id", "Time_start", "Time_end", "Date", "Class", "Course"])

                for record in records:
                    writer.writerow([
                        record.get("Lesson_id", ""),
                        record.get("Time_start", ""),
                        record.get("Time_end", ""),
                        record.get("Date", ""),
                        record.get("Class", ""),
                        record.get("Course")
                    ])

            messagebox.showinfo("Export", "Lesson information derived successfully！", parent=self.root)
            client.close()
        except Exception as es:#Python語法
            messagebox.showerror("Error", f"Due to：{str(es)}", parent=self.root)#Tkinter套件

if __name__ == "__main__":
    root = Tk()  # 窗口初始化并将根目录分配给它
    obj = InsertData(root)
    root.mainloop()  # 窗口显示