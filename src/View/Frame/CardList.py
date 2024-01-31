import tkinter as tk
from tkinter import ttk
from src.Repository.CardRepository import (
    CardRepository,
)  # Import CardRepository instead of CardGroupRepository
from .BasePage import BasePage
from .CardModalAction import CardModalAction
import tkinter.messagebox as messagebox


class CardList(BasePage):
    __card_repository = CardRepository()
    group_id: int

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        label = tk.Label(self, text="Cards", font=("Arial", 15))  # Update the label
        label.pack(pady=10)

        self.tree = ttk.Treeview(
            self, columns=("Front Text", "Back Text"), show="headings"
        )
        self.tree.heading("Front Text", text="Front Text")
        self.tree.heading("Back Text", text="Back Text")
        self.tree.pack()

        self.tree.bind("<Button-2>", self.show_popup)

        add_button = tk.Button(self, text="Add Card", command=self.add_item)
        add_button.pack()

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Edit", command=self.edit_item)
        self.popup_menu.add_command(label="Delete", command=self.delete_item)

    def delete_item(self) -> None:
        selected_item = self.tree.focus()
        if selected_item:
            self.__card_repository.delete(int(selected_item))
            self.tree.delete(selected_item)

    def add_item(self) -> None:
        modal = CardModalAction(self, title="Add Card")
        if modal.result:
            card = self.__card_repository.create(
                front_text=modal.result["front"],
                back_text=modal.result["back"],
                author=self.controller.get_user(),
                card_group_id=self.group_id,
            )
            self.tree.insert(
                "",
                tk.END,
                values=(card.front_text, card.back_text, card.next_review_after),
            )

    def edit_item(self, event=None) -> None:
        selected_item = self.tree.focus()
        if selected_item:
            card = self.__card_repository.get_by_id(int(selected_item))
            modal = CardModalAction(
                self,
                title="Edit Card",
                initial_value={"front": card.front_text, "back": card.back_text},
            )
            if modal.result:
                card.front_text = modal.result["front"]
                card.back_text = modal.result["back"]

                self.__card_repository.save()
                self.tree.item(selected_item, values=(card.front_text, card.back_text))

    def load_data(self, group_id: int, **kwargs) -> None:
        self.group_id = group_id
        self.load_cards()

    def load_cards(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
        for card in self.__card_repository.get_cards_to_study_by_group_id(
            self.group_id
        ):
            self.tree.insert(
                "",
                tk.END,
                values=(card.front_text, card.back_text, card.next_review_after),
                iid=card.id,
            )

    def show_popup(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)

            x = self.tree.winfo_rootx() + event.x
            y = self.tree.winfo_rooty() + event.y

            self.popup_menu.post(x, y)
