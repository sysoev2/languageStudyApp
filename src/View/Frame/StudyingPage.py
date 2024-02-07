import tkinter as tk
from datetime import datetime, date

from src.Repository.CardRepository import CardRepository
from src.Entity.Card import Card
from .BasePage import BasePage
from src.Observer.CardAnswerObserver import CardAnswerObserver
from supermemo2 import SMTwo
from src.Enum.CardComplexity import CardComplexity


class StudyingPage(BasePage):
    __repository = CardRepository()
    __cards: list[Card]
    __current_card: Card

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        # Main layout frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, anchor=tk.CENTER)

        self.front_text = tk.Label(self.main_frame, height=10, width=40)
        self.front_text.grid(row=1, column=0, columnspan=5)

        self.back_text = tk.Label(self.main_frame, height=10, width=40)
        self.back_text.grid(row=2, column=0, columnspan=5)

        # Frame to group action buttons
        self.action_buttons_frame = tk.Frame(self.main_frame)
        self.action_buttons_frame.grid(row=4, column=0, columnspan=5)

        self.buttons_labels = {e.value: "" for e in CardComplexity}
        for index, value in enumerate(CardComplexity):
            frame = tk.Frame(self.action_buttons_frame)
            tk.Button(
                frame, text=value.name, command=lambda v=value.value: self.__answer(v)
            ).pack()
            label = tk.Label(frame)
            self.buttons_labels[value.value] = label
            label.pack()
            frame.grid(row=0, column=index, padx=5)

        # Frame for show answer button to align using grid
        self.show_answer_frame = tk.Frame(self.main_frame)
        self.show_answer_frame.grid(row=3, column=0, columnspan=5)

        self.show_answer_button = tk.Button(
            self.show_answer_frame,
            text="Show Answer",
            command=self.__show_action_buttons,
        )
        self.show_answer_button.pack()

        self.action_buttons_frame.grid_remove()

    def __answer(self, memory: int):
        sm = SMTwo(
            self.__current_card.ease,
            (datetime.now() - self.__current_card.last_reviewed_at).days,
            self.__current_card.review_count,
        ).review(memory)
        if not sm.repetitions:
            self.__cards.insert(0, self.__current_card)
            self.__current_card.next_review_after = datetime.now()
        else:
            self.__current_card.next_review_after = sm.review_date
        self.__current_card.last_reviewed_at = datetime.now()
        self.__current_card.review_count = sm.repetitions
        self.__current_card.ease = sm.easiness
        self.__repository.save()
        self.controller.notify_observers(
            CardAnswerObserver.EVENT_NAME,
            card=self.__current_card,
            answer=int(memory),
            repeat_interval=sm.interval if sm.repetitions else 0,
        )
        if len(self.__cards) == 0:
            self.__end_game()
            return
        self.__current_card = self.__cards.pop()
        self.__show_card()

    def load_data(self, group_id: int, **kwargs) -> None:
        self.__cards = self.__repository.get_cards_to_study_by_group_id(group_id)
        if len(self.__cards) == 0:
            self.__end_game()
            return
        self.__current_card = self.__cards.pop()
        self.__show_card()

    def __show_card(self):
        self.front_text["text"] = self.__current_card.front_text
        self.back_text["text"] = ""
        self.__hide_action_buttons()

    def __end_game(self):
        self.controller.show_card_group()

    def __show_action_buttons(self):
        self.back_text["text"] = self.__current_card.back_text
        for key in self.buttons_labels:
            next_repetition = self.__estimate_next_review_date(self.__current_card, key)
            if next_repetition == 1:
                self.buttons_labels.get(key)["text"] = str(next_repetition) + " day"
            elif next_repetition > 1:
                self.buttons_labels.get(key)["text"] = str(next_repetition) + " days"
            else:
                self.buttons_labels.get(key)["text"] = "Today"
        self.show_answer_frame.grid_remove()  # Hide 'Show Answer' button frame
        self.action_buttons_frame.grid()  # Show action buttons frame

    def __hide_action_buttons(self):
        self.action_buttons_frame.grid_remove()  # Hide action buttons frame
        self.show_answer_frame.grid()  # Show 'Show

    def __estimate_next_review_date(self, card: Card, memory: int) -> int:
        sm = SMTwo(
            card.ease,
            (datetime.now() - card.last_reviewed_at).days,
            card.review_count,
        ).review(memory)
        return sm.repetitions if sm.interval else 0
