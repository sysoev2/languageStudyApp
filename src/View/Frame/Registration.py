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

        register_button = tk.Button(self, text="Register", command=self.__register_user)
        register_button.pack()

        login_button = tk.Button(
            self,
            text="Back to Login",
            command=self.__redirect_to_login,
        )
        login_button.pack()

    def __register_user(self) -> None:
        user = self.__save_user()
        if user is None:
            return

        self.controller.set_user(user)
        self.__clear_inputs()

    def __save_user(self) -> User | None:
        dto = UserDTO(
            username=self.username.get(),
            password=self.password.get(),
            password_repeat=self.password_repeat.get(),
        )
        if not self.__validate_user(dto):
            return
        user = User.create_from_dto(dto)
        self.__repository.persist(user)
        self.__repository.save()
        return user

    def __clear_inputs(self):
        self.username.clear()
        self.password.clear()
        self.password_repeat.clear()

    def __redirect_to_login(self) -> None:
        self.controller.show_login()
        self.__clear_inputs()

    def __validate_user(self, user_dto: UserDTO) -> bool:
        errors = UserDTOValidator().validate(user_dto)
        if errors is not True:
            ValidatorErrorsHelper.show_errors(errors)
            return False
        return True
