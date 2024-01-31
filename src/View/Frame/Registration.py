import tkinter as tk
from src.Entity.User import User
from .BasePage import BasePage
from src.View.Component.Input import Input
from ...DTO.UserDTO import UserDTO
from ...Repository.UserRepository import UserRepository
from ...Validator.EntityValidator.UserDTOValidator import UserDTOValidator
from ...Validator.ValidatorErrorsHelper import ValidatorErrorsHelper


class RegisterFrame(BasePage):
    __repository = UserRepository()

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

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
            command=self.redirect_to_login,
        )
        login_button.pack()

    def register_user(self) -> None:
        user = self.save_user()
        if user is None:
            return

        self.controller.set_user(user)
        self.clear_inputs()

    def save_user(self) -> User | None:
        dto = UserDTO(
            username=self.username.get(),
            password=self.password.get(),
            password_repeat=self.password_repeat.get(),
        )
        if not self.validate_user(dto):
            return
        user = User.create_from_dto(dto)
        self.__repository.persist(user)
        self.__repository.save()
        return user

    def clear_inputs(self):
        self.username.clear()
        self.password.clear()
        self.password_repeat.clear()

    def redirect_to_login(self) -> None:
        self.controller.show_login()
        self.clear_inputs()

    def validate_user(self, user_dto: UserDTO) -> bool:
        errors = UserDTOValidator().validate(user_dto)
        if errors is not True:
            ValidatorErrorsHelper.show_errors(errors)
            return False
        return True
