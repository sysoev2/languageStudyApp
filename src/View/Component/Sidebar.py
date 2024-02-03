import tkinter as tk
from tkinter import ttk

selectionbar_color = "#eff5f6"
sidebar_color = "#F5E1FD"
header_color = "#53366b"
visualisation_frame_color = "#ffffff"


class Sidebar(tk.Frame):
    """
    A submenu which can have multiple options and these can be linked with
    functions.
    """

    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        """
        parent: The frame where submenu is to be placed
        sub_menu_heading: Heading for the options provided
        sub_menu_operations: Options to be included in sub_menu
        """
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(
            self,
            text=sub_menu_heading,
            bg=sidebar_color,
            fg="#333333",
            font=("Arial", 10),
        )
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient="horizontal")
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(
                self,
                text=x,
                bg=sidebar_color,
                font=("Arial", 9, "bold"),
                bd=0,
                cursor="hand2",
                activebackground="#ffffff",
                highlightbackground=sidebar_color,
            )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")
