import tkinter as tk
from tkinter import ttk

from src.Observer.UserLoginObserver import UserLoginObserver
from src.View.Frame.AddCard import AddCard
from src.View.Frame.Login import LoginFrame
from src.View.Frame.Registration import RegisterFrame
from src.View.Frame.CardGroup import CardGroup
from src.View.Frame.StudyingPage import StudyingPage
from index.database import Database
from src.Entity.User import User
from sqlalchemy.orm import Session
from src.Observable.AbstractObservable import AbstractObservable

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = "#eff5f6"
sidebar_color = "#F5E1FD"
header_color = "#53366b"
visualisation_frame_color = "#ffffff"


# ------------------------------- ROOT WINDOW ----------------------------------


class TkinterApp(tk.Tk, AbstractObservable):
    __user: User | None
    __session: Session

    def __init__(self):
        tk.Tk.__init__(self)
        AbstractObservable.__init__(self)
        database = Database()
        database.create_tables()
        self.__session = database.get_session()
        self.title("Anki card application")

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        self.resizable(0, 0)
        self.title("Attendance Tracking System")
        self.config(background=selectionbar_color)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # UNIVERSITY LOGO AND NAME
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        uni_name = tk.Label(
            self.brand_frame, text="Anki cards", bg=sidebar_color, font=("", 15, "bold")
        )
        uni_name.place(x=55, y=60, anchor="w")

        # SUBMENUS IN SIDE BAR
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=2)
        self.submenu1 = Sidebar(
            self.submenu_frame,
            sub_menu_heading="SUBMENU 1",
            sub_menu_options=["Display Card Group", "Display Add Card", "Logout"],
        )
        self.submenu1.options["Display Card Group"].config(
            command=lambda: self.show_card_group()
        )
        self.submenu1.options["Display Add Card"].config(
            command=lambda: self.show_add_card()
        )
        self.submenu1.options["Logout"].config(command=lambda: self.logout())

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        for F in (
            LoginFrame,
            RegisterFrame,
            CardGroup,
            AddCard,
            StudyingPage,
        ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_login()

    def show_sidebar(self):
        self.submenu1.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

    def hide_sidebar(self):
        self.submenu1.place_forget()

    def _show_frame(self, cont, **kwargs):
        frame = self.frames[cont]
        frame.tkraise()
        frame.load_data(**kwargs)

    def show_login(self) -> None:
        self._show_frame(LoginFrame)

    def show_register(self) -> None:
        self._show_frame(RegisterFrame)

    def show_card_group(self) -> None:
        self._show_frame(CardGroup)

    def show_add_card(self) -> None:
        self._show_frame(AddCard)

    def show_studying_page(self, group_id: int) -> None:
        self._show_frame(StudyingPage, group_id=group_id)

    def get_user(self) -> None | User:
        return self.__user

    def set_user(self, user: User) -> None:
        self.__user = user
        self.notify_observers(user=user)

    def logout(self) -> None:
        self.__user = None
        self.notify_observers(user=None)

    def get_session(self) -> Session:
        return self.__session


# ------------------------ MULTIPAGE FRAMES AND SIDEBAR ------------------------------------


class Sidebar(tk.Frame):
    def __init__(self, parent, sub_menu_heading, sub_menu_options):
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
            )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")


# ------------------------ MAIN APP EXECUTION ------------------------------------
if __name__ == "__main__":
    app = TkinterApp()

    app.add_observer(UserLoginObserver())

    app.mainloop()
