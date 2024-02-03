import tkinter as tk
from typing import Type

from src.Entity.CardsGroup import CardsGroup
from src.Observer.UserLoginObserver import UserLoginObserver
from src.Observer.CardAnswerObserver import CardAnswerObserver
from src.View.Component.Sidebar import Sidebar
from src.View.Frame.CardList import CardList
from src.View.Frame.StudyingHistory import StudyingHistory
from src.View.Frame.AddCard import AddCard
from src.View.Frame.BasePage import BasePage
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
        self.title("Card learning app")

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        self.resizable(0, 0)
        self.title("Card learning app")
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
            self.brand_frame,
            text="Card learning app",
            bg=sidebar_color,
            font=("", 15, "bold"),
        )
        uni_name.place(x=55, y=60, anchor="w")

        # SUBMENUS IN SIDE BAR
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=2)
        self.submenu1 = Sidebar(
            self.submenu_frame,
            sub_menu_heading="Menu",
            sub_menu_options=[
                "Display Card Group",
                "Display Add Card",
                "Studying Log",
                "Logout",
            ],
        )
        self.submenu1.options["Display Card Group"].config(
            command=lambda: self.show_card_group()
        )
        self.submenu1.options["Display Add Card"].config(
            command=lambda: self.show_add_card()
        )
        self.submenu1.options["Studying Log"].config(
            command=lambda: self.show_studying_history()
        )
        self.submenu1.options["Logout"].config(command=lambda: self.logout())

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        F: Type[BasePage]
        for F in (
            LoginFrame,
            RegisterFrame,
            CardGroup,
            AddCard,
            StudyingPage,
            StudyingHistory,
            CardList,
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

    def show_studying_history(self) -> None:
        self._show_frame(StudyingHistory)

    def show_studying_page(self, group_id: int) -> None:
        self._show_frame(StudyingPage, group_id=group_id)

    def show_card_list(self, group: CardsGroup) -> None:
        self._show_frame(CardList, group=group)

    def get_user(self) -> None | User:
        return self.__user

    def set_user(self, user: User) -> None:
        self.__user = user
        self.notify_observers(UserLoginObserver.EVENT_NAME, user=user)

    def logout(self) -> None:
        self.__user = None
        self.notify_observers(UserLoginObserver.EVENT_NAME, user=None)

    def get_session(self) -> Session:
        return self.__session


# ------------------------ MAIN APP EXECUTION ------------------------------------
if __name__ == "__main__":
    app = TkinterApp()

    app.add_observer(UserLoginObserver())
    app.add_observer(CardAnswerObserver())

    app.mainloop()
