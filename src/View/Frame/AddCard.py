import tkinter as tk
from src.Repository.CardRepository import CardRepository
from src.Repository.CardGroupRepository import CardGroupRepository
from .BasePage import BasePage
from tkinter import ttk
from src.Entity.Card import Card
from src.Validator.EntityValidator.CardValidator import CardValidator
from src.View.Component.Input import Input
from src.Validator.ValidatorErrorsHelper import ValidatorErrorsHelper


class AddCard(BasePage):
    __repository = CardRepository()
    groups = []

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Add Card", font=("Arial", 15))
        label.pack(pady=10)

        self.front_text = Input(self, "Front Text")
        self.front_text.pack()

        self.back_text = Input(self, "Back Text")
        self.back_text.pack()

        self.card_groups = ttk.Combobox(self, state="readonly")
        self.card_groups.pack()

        add_button = tk.Button(self, text="Add Card", command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=(0, 10))

    def add_item(self) -> None:
        if self.card_groups.current() < 0:
            ValidatorErrorsHelper.show_errors({"Card group": "Please select a group"})
            return
        card = Card(
            front_text=self.front_text.get(),
            back_text=self.back_text.get(),
            author=self.controller.get_user(),
            card_group=self.groups[self.card_groups.current()],
        )
        if not self.validate_card(card):
            return
        self.__repository.persist(card)
        self.__repository.save()
        self.front_text.delete(0, tk.END)
        self.back_text.delete(0, tk.END)

    def load_data(self) -> None:
        self.card_groups.set("")
        self.card_groups["values"] = []
        self.groups = []
        values = []
        for group in CardGroupRepository().get_all_by(user=self.controller.get_user()):
            self.groups.append(group)
            values.append(group.name)
        self.card_groups["values"] = values
        if values:
            self.card_groups.current(0)

    def validate_card(self, card: Card) -> bool:
        errors = CardValidator().validate(card)
        if errors is not True:
            ValidatorErrorsHelper.show_errors(errors)
            return False
        return True
