import tkinter as tk
from src.Entity.User import User
from .BasePage import BasePage
from src.View.Component.Input import Input


class RegisterFrame(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Register", font=("Arial", 15))
        label.pack(pady=10)

        self.username = Input(self, "Username")
        self.username.pack()

        self.password = Input(self, "Password", show="*")
        self.password.pack()

        self.password_repeat = Input(self, "Repeat Password", show="*")
        self.password_repeat.pack()

        register_button = tk.Button(self, text="Register", command=self.register_user)
        register_button.pack()

        login_button = tk.Button(
            self,
            text="Back to Login",
            command=self.show_login,
        )
        login_button.pack()

    def register_user(self) -> None:
        user = User(username=self.username.get(), password=self.password.get())
        session = self.controller.get_session()
        session.add(user)
        session.commit()
        self.controller.set_user(user)
        self.clear_inputs()

    def clear_inputs(self):
        self.username.clear()
        self.password.clear()
        self.password_repeat.clear()

    def show_login(self) -> None:
        self.controller.show_login()
        self.clear_inputs()
