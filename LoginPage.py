from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from time import strftime
from main_upd import Face_Recognition_System
from main_upd import new_print
from pymongo import MongoClient

class LoginPage(object):
    # hàm khởi tạo giao diện
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')#kích thước giao diện
        self.window.resizable(0, 0) #ko cho giao diện thu nhỏ
        self.window.state('zoomed') #giao diện hiển thị toàn màn hình
        self.window.title('Login to the System') #tiêu đề của cửa sổ app
        self.window.iconbitmap('ImageFaceDetect\\gaming.ico')
        today = strftime("%d-%m-%Y")  # thời gian ngày-tháng-năm

        # =============biến kiểu string email,password============
        self.var_email = StringVar()
        self.var_password = StringVar()

        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('ImageFaceDetect\\background1.png')#khai báo biến bg_frame là ảnh background trong thư mục ImageFaceDetect\\background1.png
        photo = ImageTk.PhotoImage(self.bg_frame)# chuyển ảnh về lớp ImageTk
        self.bg_panel = Label(self.window, image=photo)#Khai báo biến bg_panel chứa ảnh photo
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')#Vị trí của lớp Label : chính giữa giao diện
        # ====== Login Frame =========================

        self.lgn_frame = Frame(self.window, bg='#C0C0C0', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)

        # ========================================================================
        # ========================================================
        # ======Hiện thị ngày====
        self.txt = today
        self.heading = Label(self.lgn_frame, text=self.txt, font=('times new roman', 25, "bold"), bg="#C0C0C0",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('ImageFaceDetect\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#C0C0C0')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('ImageFaceDetect\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#C0C0C0')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=630, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Login", bg="#C0C0C0", fg="white",
                                    font=("times new roman", 17, "bold"))
        self.sign_in_label.place(x=670, y=240)

        # ========================================================================
        # ============================tài khoản====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Account", bg="#C0C0C0", fg="white",
                                    font=("times new roman", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.txtuser = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#C0C0C0", fg="#E5E4E2",
                                    font=("times new roman ", 12, "bold"),textvariable=self.var_email)
        self.txtuser.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#E5E4E2", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('ImageFaceDetect\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#C0C0C0')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ========================================================================
        # ============================Nút đăng nhập================================
        # ========================================================================
        self.lgn_button = Image.open('ImageFaceDetect\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#C0C0C0')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='Log In',command=self.login_action,
                            font=("times new roman", 15, "bold"), width=10, bd=0,
                            bg='#acd2d2', cursor='hand2', activebackground='#3D4755', fg='white')
        self.login.place(x=83, y=10)

        # Bind Enter key to log in function
        self.window.bind('<Return>', lambda event=None: self.login_action())


        # =============check_button=============
        self.varcheck = IntVar()
        checkbtn = Checkbutton(self.lgn_frame, variable=self.varcheck,
                               font=("times new roman", 12), onvalue=1, offvalue=0 ,bg="#C0C0C0"
                                )
        checkbtn.place(x=550, y=510)

        self.check_label = Label(self.lgn_frame, text=" Log in as Admin", bg="#C0C0C0", fg="white",relief=FLAT,
                                    font=("times new roman", 12, "bold"))
        self.check_label.place(x=580, y=513)

        # ========================================================================
        # ============================Mật khẩu====================================
        # ========================================================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#C0C0C0", fg="white",
                                    font=("times new roman", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.txtpass = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#C0C0C0", fg="white",
                                    font=("times new roman", 12, "bold"), show="*",textvariable=self.var_password)
        self.txtpass.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#E5E4E2", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================
        self.password_icon = Image.open('ImageFaceDetect\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#C0C0C0')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password ==================================================================
        #ảnh nút hiển thị password
        self.show_image = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\show.png')

        #ảnh  nút ẩn password
        self.hide_image = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\hide.png')

        #nút hiển thị password
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.showpass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def showpass(self):#hàm hiển thị mật khẩu
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.txtpass.config(show='')
    def show(self):
        """"""
        self.window.update()
        self.window.deiconify()
    def hide(self):#hàm ẩn mật khẩu dưới dạng ***
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.showpass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.txtpass.config(show='*')

    #reset thông tin password_tài khoản
    def reset(self):
        self.var_email.set("")
        self.var_password.set("")
        self.varcheck.set(0)

    # hàm đăng nhập
    def login_action(self):

        # 建立MongoDB連線
        client = MongoClient(
            "mongodb+srv://LittleAssChild:c19850505s970194@cluster0.lmtseyw.mongodb.net/")
        # 指定資料庫
        db = client["Face_Recognizer"]
        # 指定集合（collection）

        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error!!","Please enter complete information.")
        elif(self.varcheck.get()==1) :
            try:
                admin_collection = db['admin']  # 替換為你的admin集合名稱
                admin_doc = admin_collection.find_one({
                    'Account': self.var_email.get(),
                    'Password': self.var_password.get()
                })
                if admin_doc is None:
                    messagebox.showerror("Error", "Wrong username, password or login permission")
                else:
                    new_print(str(0))
                    # # self.window.destroy()
                    # # import home
                    self.reset()
                    messagebox.showinfo("Notification","You have successfully logged in as an Admin!!")
                    self.window.withdraw()
                    # self.new_window = Toplevel(self.window)

                    self.app = Face_Recognition_System(self)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self)
        else:
            try:
                teacher_collection = db['teacher']  # 替換為你的teacher集合名稱
                teacher_doc = teacher_collection.find_one({
                    'Email': self.var_email.get(),
                    'Password': self.var_password.get()
                })
                if teacher_doc is None:
                    messagebox.showerror("Error", "Incorrect username or password!!")
                else:
                    new_print(str(teacher_doc['Teacher_id']))
                    self.reset()
                    self.window.withdraw()
                    self.app = Face_Recognition_System(self)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self)





if __name__ == '__main__':
    window = Tk()  # tạo giao diện tkinter Tk() và gán nó vào biến window
    obj = LoginPage(window)
    window.mainloop()  # hiển thị giao diện và bắt đầu nhận các sự kiện để xử lý.