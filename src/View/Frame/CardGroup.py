import tkinter as tk
from src.Repository.CardGroupRepository import CardGroupRepository
from .BasePage import BasePage
from .StudyingPage import StudyingPage


class CardGroup(BasePage):
    __repository = CardGroupRepository()
    items: list

    def __init__(self, parent, controller):
        BasePage.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Card Groups", font=("Arial", 15))
        label.pack(pady=10)

        self.groups = tk.Listbox(self)
        self.groups.pack()
        self.entry = tk.Entry(self)
        self.entry.pack()

        add_button = tk.Button(self, text="Add Item", command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=(0, 10))

        delete_button = tk.Button(self, text="Delete Item", command=self.delete_item)
        delete_button.pack(side=tk.RIGHT)

        edit_button = tk.Button(self, text="Edit Item", command=self.edit_item)
        edit_button.pack(side=tk.LEFT)

        edit_button = tk.Button(self, text="Study", command=self.start_learning)
        edit_button.pack(side=tk.LEFT)

    def add_item(self) -> None:
        self.__repository.create(name=self.entry.get(), user=self.controller.get_user())
        self.groups.insert(tk.END, self.entry.get())

    def delete_item(self) -> None:
        item = self.items[self.groups.curselection()[0]]
        self.__repository.delete(item)
        self.items.remove(item)
        self.groups.delete(tk.ANCHOR)

    def edit_item(self) -> None:
        selected = self.groups.curselection()

        if selected:
            group = self.items[selected[0]]
            group.name = self.entry.get()
            self.groups.delete(selected[0])
            self.groups.insert(selected[0], self.entry.get())
            self.__repository.save()

    def load_data(self, **kwargs) -> None:
        self.groups.delete(0, tk.END)
        self.items = []
        for group in self.__repository.get_all_by(user=self.controller.get_user()):
            self.items.append(group)
            self.groups.insert(group.id, group.name)

    def start_learning(self):
        self.controller.show_frame(
            StudyingPage, group_id=self.items[self.groups.curselection()[0]].id
        )
