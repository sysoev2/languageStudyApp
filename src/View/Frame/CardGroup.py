import tkinter as tk
from tkinter import ttk
from src.Repository.CardGroupRepository import CardGroupRepository
from src.Repository.CardRepository import CardRepository
from .BasePage import BasePage
from .CardGroupModalAction import ModalWindow
import tkinter.messagebox as messagebox


class CardGroup(BasePage):
    __repository = CardGroupRepository()
    __card_repository = CardRepository()

    def __init__(self, parent, controller):
        BasePage.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Card Groups", font=("Arial", 15))
        label.pack(pady=10)

        # Setting up the Treeview with additional columns
        self.tree = ttk.Treeview(self, columns=("Name", "ActiveCard"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("ActiveCard", text="Active Card")
        self.tree.pack()

        self.tree.bind("<Button-2>", self.show_popup)
        self.tree.bind("<Return>", self.start_learning)

        add_button = tk.Button(self, text="Add Item", command=self.add_item)
        add_button.pack()

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Edit", command=self.edit_item)
        self.popup_menu.add_command(label="Delete", command=self.delete_item)

    def delete_item(self) -> None:
        selected_item = self.tree.focus()
        if selected_item:
            self.__repository.delete(int(selected_item))
            self.tree.delete(selected_item)

    def add_item(self) -> None:
        modal = ModalWindow(self, title="Add Card Group")
        if modal.result:
            group = self.__repository.create(
                name=modal.result, user=self.controller.get_user()
            )
            self.tree.insert("", tk.END, values=(group.name, 0))

    def edit_item(self, event=None) -> None:
        selected_item = self.tree.focus()
        if selected_item:
            group = self.__repository.get_by_id(int(selected_item))
            modal = ModalWindow(self, title="Edit Card Group", initial_value=group.name)
            if modal.result:
                group.name = modal.result
                # Update the repository and the treeview item
                self.__repository.save()
                self.tree.item(
                    selected_item,
                    values=(group.name, self.tree.item(selected_item, "values")[1]),
                )

    def load_data(self, **kwargs) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
        for group in self.__repository.get_all_by(user=self.controller.get_user()):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    group.name,
                    self.__card_repository.get_cards_to_study_by_group_name_count(
                        group.id
                    ),
                ),
                iid=group.id,
            )

    def start_learning(self, event=None) -> None:
        selected_item = self.tree.focus()
        if selected_item and int(self.tree.item(selected_item, "values")[1]) > 0:
            self.controller.show_studying_page(int(selected_item))
            return
        messagebox.showerror(
            "Error",
            "No active cards available for this group at the moment. Cards will become available again over "
            "time. Please check back later.",
            parent=self,
        )

    def show_popup(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)

            x = self.tree.winfo_rootx() + event.x
            y = self.tree.winfo_rooty() + event.y

            self.popup_menu.post(x, y)