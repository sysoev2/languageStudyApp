import tkinter as tk
from src.Repository.CardRepository import CardRepository
from src.Repository.CardGroupRepository import CardGroupRepository
from .BasePage import BasePage
from tkinter import ttk


class AddCard(BasePage):
    __repository = CardRepository()
    groups = []

    def __init__(self, parent, controller):
        BasePage.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Add Card", font=("Arial", 15))
        label.pack(pady=10)

        self.front_text = tk.Entry(self)
        self.front_text.pack()

        self.back_text = tk.Entry(self)
        self.back_text.pack()

        self.card_groups = ttk.Combobox(self)
        self.card_groups.pack()

        add_button = tk.Button(self, text="Add Card", command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=(0, 10))

    def add_item(self) -> None:
        self.__repository.create(
            front_text=self.front_text.get(),
            back_text=self.back_text.get(),
            author=self.controller.get_user(),
        )
        self.front_text.delete(0, tk.END)
        self.back_text.delete(0, tk.END)

    def load_data(self) -> None:
        self.card_groups["values"] = []
        values = []
        for group in CardGroupRepository().get_all_by(user=self.controller.get_user()):
            self.groups.append(group)
            values.append(group.name)
        self.card_groups["values"] = values
