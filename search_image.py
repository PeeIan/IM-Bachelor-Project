import base64
import os
import re
import pymongo
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import PIL
from PIL import ImageTk, Image
from database_str import Database_str
from pymongo import MongoClient
from io import BytesIO
value_from_student=None


def student_id(value):
    global value_from_student
    value_from_student = value
    print(value_from_student)



class StdImage:
    def __init__(self,root):
        self.root = root
        self.root.geometry("800x600+300+50")
        self.root.title("Student Photo Management")
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # icon của giao diện

        # thông tin kết nối database
        self.db = Database_str()

        Left_frame = Frame(root, bd=2, bg="white")
        Left_frame.place(x=20, y=10, width=200, height=550)

        self.lst = tk.Listbox(Left_frame, width=20)
        self.lst.pack(side="left", fill=tk.BOTH, expand=0)
        self.lst.place(x=20,y=20,width=150,height=500)
        self.lst.bind("<<ListboxSelect>>", self.showimg)

        sbr=tk.Scrollbar(Left_frame)
        sbr.pack(side=RIGHT,fill="y")
        sbr.config(command=self.lst.yview)

        self.lst.config(yscrollcommand=sbr.set)

        right_fr = LabelFrame(root, bd=2, bg="white", relief=RIDGE, text="Student Information",
                                          font=("times new roman", 12, "bold"))
        right_fr.place(x=230, y=10, width=560, height=550)



        #student info
        self.Student_id_label = Label(right_fr, text="Student ID:",
                                     font=("times new roman", 12, "bold"), bg="white")
        self.Student_id_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.Student_id_atten_label = Label(right_fr, text="", font=("times new roman", 12, "bold"),
                                           bg="white", fg="red2")
        self.Student_id_atten_label.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # name
        self.stdName_label = Label(right_fr, text="Student name:",
                                          font=("times new roman", 12, "bold"),
                                          bg="white")
        self.stdName_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.stdName_atten_label = Label(right_fr, text="", font=("times new roman", 12, "bold"),
                                                bg="white", fg="red2")
        self.stdName_atten_label.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # class
        self.class_label = Label(right_fr, text="Regular class:",
                                     font=("times new roman", 12, "bold"),
                                     bg="white")
        self.class_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        self.class_atten_label = Label(right_fr, text="",
                                           font=("times new roman", 12, "bold"),
                                           bg="white", fg="red2")
        self.class_atten_label.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # getStudentInfo
        # Query using a projection to retrieve only relevant fields
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        student_collection = db['student']
        query = {"Student ID": int(value_from_student)}
        projection = {"_id": 0, "Student ID": 1, "Student name": 1, "Course": 1}  # Exclude _id field
        getInfo = student_collection.find_one(query, projection)

        self.Student_id_atten_label['text'] = getInfo["Student ID"]
        self.stdName_atten_label['text'] = getInfo["Student name"]
        self.class_atten_label['text'] = getInfo["Course"]

        #image_frame
        img_fr = LabelFrame(right_fr, bd=2, bg="white", relief=RIDGE)
        img_fr.place(x=170, y=120, width=235, height=235)

        #image
        self.insertfiles()
        self.canvas = tk.Canvas(img_fr)
        self.canvas.place(x=5,y=5)

        save_btn=Button(right_fr,text="Delete photo",command=self.delete,font=("times new roman",13,"bold"),bg="#000000", fg="white",width=17)
        save_btn.place(x=100,y=450)
        delete_all_btn = Button(right_fr,text="Delete all photo",command=self.delete_all,font=("times new roman",13,"bold"),bg="#000000", fg="white",width=17)
        delete_all_btn.place(x=300,y=450)

    #================Functions=====================
    def insertfiles(self):
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        student_collection = db['student']
        getInfo = student_collection.find_one(
            {"Student ID": int(value_from_student)},
            {"Student name": 1, "Student ID": 1, "_id": 0}
        )

        if getInfo:
            directory = "student_photo"

            # 檢查目錄是否存在
            if os.path.exists(directory):
                file_names = os.listdir(directory)

                num = 0
                for file_name in file_names:
                    id = int(os.path.split(file_name)[1].split('_')[0])  # 從圖片的名稱中提取出學生的ID（例如：user.1.19.jpg -> 學生ID = 1）
                    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")) and id == getInfo["Student ID"]:
                        full_path = os.path.join(directory, file_name)
                        num += 1
                        self.lst.insert(tk.END, full_path)

                print("Number of photos taken: " + str(num))
            else:
                print(f"Directory not found: {directory}")











    def showimg(self, event):
        n = self.lst.curselection()
        if n:
            index = n[0]
            filename = self.lst.get(index)

            self.img_right = PIL.Image.open(filename)
            self.img_right = self.img_right.resize((220, 220), PIL.Image.ANTIALIAS)

            img = ImageTk.PhotoImage(self.img_right)
            # img = ImageTk.PhotoImage(file=filename)

            w, h = img.width(), img.height()
            print(filename)
            self.canvas.image = img
            self.canvas.config(width=w, height=h)
            self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
        else:
            print("No image selected")

    def delete(self):

        Exit = messagebox.askyesno("Delete photo", "Are you sure you want to delete this photo?", parent=self.root)
        if (Exit > 0):
            client = MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["Face_Recognizer"]
            student_collection = db['student']
            getInfo = student_collection.find_one(
                {"Student ID": int(value_from_student)},
                {"Student ID": 1, "Student name": 1, "_id": 0}
            )
            id = getInfo["Student ID"]
            name = getInfo["Student name"]
            n = self.lst.curselection()  # 獲取當前被選擇的列表框中的項目的索引
            filename = self.lst.get(n)  # 從列表框中取得被選擇項目的內容（通常是文字），並將這個內容存儲在filename變數中
            print(filename)
            os.remove(filename)  # 刪除具有指定名稱或路徑的檔案
            self.lst.delete(n)  # clear listbox

            # 使用正則表達式來匹配數字部分
            match = re.search(r'\d+', filename)

            # 檢查是否找到匹配
            if match:
                # 從匹配的結果中獲取數字部分
                number_part = match.group()
                print("數字部分:", number_part)
            else:
                print("找不到數字部分")

            print(type(number_part))
            client = pymongo.MongoClient(
                "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
            # 指定資料庫
            db = client["student_photo"]
            # 指定集合（collection）
            collection = db[f"{name}"]
            # 删除符合条件的单个文档
            query = {"photo_id": int(number_part)}

            try:
                result = collection.delete_one(query)
                print(result.deleted_count, "已删除")
            except Exception as e:
                print("删除操作失败:", str(e))

            print("number of photos taken :" + str(self.lst.size()))
            print("You have just deleted a photo " + filename)


        else:
            if not Exit:
                return

    def delete_all(self):
        try:
            delete = messagebox.askyesno("Delete all photo", "Do you want to delete all photo of this student?",
                                         parent=self.root)
            if delete > 0:
                client = MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["Face_Recognizer"]
                student_collection = db['student']
                getInfo = student_collection.find_one(
                    {"Student ID": int(value_from_student)},
                    {"Student name": 1, "Student ID": 1, "_id": 0}
                )

                mongo_photo = str(getInfo["Student ID"]) + "_" + getInfo["Student name"]
                folder_name = "student_photo"
                for file in os.listdir(folder_name):
                    file_path = os.path.join(folder_name, file)
                    print(type(file_path))
                    # 檢查檔名是否包含"1_face_1"，且學生id等於1
                    if f"{getInfo['Student ID']}_face_" in file_path:
                        try:
                            os.remove(file_path)
                            print(f'File {file} deleted successfully!')
                        except OSError as e:
                            print(f'Error: {file} deletion failed. - {e}')

                # 建立MongoDB連線
                client = pymongo.MongoClient(
                    "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
                # 指定資料庫
                db = client["student_photo"]
                # 指定集合（collection）
                collection = db[f"{mongo_photo}"]

                # 删除数据库
                collection.drop()

                print(f'集合 {collection} 已成功删除')

            else:
                if not delete:
                    return

            #self.fetch_data()
            #self.reset_data()
            messagebox.showinfo("Delete", "Delete student successfully", parent=self.root)
            self.lst.delete(0, tk.END)
            self.canvas.delete("all")
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)


if __name__=="__main__":
    root = Tk()  # Initialize the window and assign root
    obj = StdImage(root)
    root.mainloop()  # Show window
