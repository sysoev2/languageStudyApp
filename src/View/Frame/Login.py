import tkinter as tk
from src.Repository.UserRepository import UserRepository
import bcrypt
from .BasePage import BasePage
from src.View.Component.Input import Input
from tkinter import messagebox


class LoginFrame(BasePage):
    __repository = UserRepository()

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Login", font=("Arial", 15))
        label.pack(pady=10)

        self.username = Input(self, "Username")
        self.username.pack()

        self.password = Input(self, "Password", show="*")
        self.password.pack()

        login_button = tk.Button(self, text="Login", command=self.__login_user)
        login_button.pack()

        register_button = tk.Button(
            self, text="Register", command=lambda: controller.show_register()
        )
        register_button.pack()

    def __login_user(self):
        user = self.__repository.get_one_by(username=self.username.get())
        if user is not None and bcrypt.checkpw(
            self.password.get().encode("utf-8"), user.password
        ):
            self.controller.set_user(user)
            self.__clear_inputs()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def __clear_inputs(self):
        self.username.clear()
        self.password.clear()
