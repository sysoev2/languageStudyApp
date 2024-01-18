import tkinter as tk
from src.Entity.User import User
from .BasePage import BasePage


class RegisterFrame(BasePage):
    def __init__(self, parent, controller):
        from .Login import LoginFrame

        BasePage.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Register", font=("Arial", 15))
        label.pack(pady=10)

        self.username = tk.Entry(self)
        self.username.pack()

        self.password = tk.Entry(self, show="*")
        self.password.pack()

        register_button = tk.Button(self, text="Register", command=self.register_user)
        register_button.pack()

        login_button = tk.Button(
            self, text="Back to Login", command=controller.show_frame(LoginFrame)
        )
        login_button.pack()

    def register_user(self) -> None:
        user = User(username=self.username.get(), password=self.password.get())
        session = self.controller.get_session()
        session.add(user)
        session.commit()
