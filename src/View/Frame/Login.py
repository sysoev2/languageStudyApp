import tkinter as tk
from .Registration import RegisterFrame
from src.Repository.UserRepository import UserRepository
import bcrypt


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text='Login', font=("Arial", 15))
        label.pack(pady=10)

        self.username = tk.Entry(self)
        self.username.pack()

        self.password = tk.Entry(self, show='*')
        self.password.pack()

        login_button = tk.Button(self, text='Login', command=self.login_user)
        login_button.pack()

        register_button = tk.Button(self, text='Register', command=lambda: controller.show_frame(RegisterFrame))
        register_button.pack()

    def login_user(self):
        user = UserRepository().get_one_by(username=self.username.get())
        if user is not None and bcrypt.checkpw(self.password.get().encode('utf-8'), user.password):
            self.controller.set_user(user)


