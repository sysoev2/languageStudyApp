import tkinter as tk
from tkinter import ttk
from src.Repository.StudyingLogRepository import StudyingLogRepository
from src.Repository.CardGroupRepository import CardGroupRepository
from .BasePage import BasePage
from src.Enum.CardComplexity import CardComplexity


class StudyingHistory(BasePage):
    __studying_log_repository: StudyingLogRepository

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.__studying_log_repository = StudyingLogRepository()

        self.tree = ttk.Treeview(
            self,
            columns=("Date", "Card Group", "Reviewed Cards Count"),
            show="headings",
        )
        self.tree.heading("Date", text="Date")
        self.tree.heading("Card Group", text="Card Group")
        self.tree.heading("Reviewed Cards Count", text="Reviewed Cards Count")
        self.tree.bind("<Double-1>", self.__on_item_double_click)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_data(self, **kwargs) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
        for session in self.__studying_log_repository.get_log_group_by_day(
            self.controller.get_user().id
        ):
            self.tree.insert(
                "",
                tk.END,
                values=(session.date, session.name, session.count, session.id),
                iid=None,
            )

    def __on_item_double_click(self, event):
        item_id = self.tree.selection()[0]
        session_details = self.tree.item(item_id)["values"]
        self.__show_session_detail(
            session_details[0], session_details[1], session_details[3]
        )

    def __show_session_detail(self, date: str, card_group: str, card_group_id: int):
        detail_window = tk.Toplevel(self)
        detail_window.grab_set()
        label = tk.Label(detail_window, text=f"Details for {date}, {card_group}")
        tree = ttk.Treeview(
            detail_window,
            columns=("id", "front_text", "back_text", "answer", "next_review_interval"),
            show="headings",
        )
        tree.heading("id", text="Id")
        tree.heading("front_text", text="Front Text")
        tree.heading("back_text", text="Back Text")
        tree.heading("answer", text="Answer")
        tree.heading("next_review_interval", text="Next in (days)")
        tree.pack(fill=tk.BOTH, expand=True)
        for log in self.__studying_log_repository.get_logs_by_card_group_id_and_date(
            int(card_group_id), date
        ):
            tree.insert(
                "",
                tk.END,
                values=(
                    log.card.id,
                    log.card.front_text,
                    log.card.back_text,
                    CardComplexity(log.answer).name,
                    log.repeat_interval,
                ),
            )
        label.pack()
