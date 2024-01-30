import tkinter as tk
from datetime import datetime

from src.Repository.CardRepository import CardRepository
from src.Entity.Card import Card
from .BasePage import BasePage
from src.Observer.CardAnswerObserver import CardAnswerObserver
from supermemo2 import SMTwo
from src.Enum.CardComplexity import CardComplexity


class StudyingPage(BasePage):
    __repository = CardRepository()
    cards: list[Card]
    current_card: Card

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        label = tk.Label(self, text="Studying", font=("Arial", 15))
        label.pack(pady=10)

        self.front_text = tk.Label(self, height=10, width=40)
        self.front_text.pack()

        self.back_text = tk.Label(self, height=10, width=40)
        self.back_text.pack()

        self.again_button = tk.Button(
            self, text="Again", command=lambda: self.answer(CardComplexity.Again.value)
        )

        self.bad_button = tk.Button(
            self, text="Bad", command=lambda: self.answer(CardComplexity.Bad.value)
        )

        self.good_button = tk.Button(
            self, text="Good", command=lambda: self.answer(CardComplexity.Good.value)
        )

        self.easy_button = tk.Button(
            self, text="Easy", command=lambda: self.answer(CardComplexity.Easy.value)
        )

        self.perfect_button = tk.Button(
            self,
            text="Perfect",
            command=lambda: self.answer(CardComplexity.Perfect.value),
        )

        self.show_answer_button = tk.Button(
            self, text="Show Answer", command=self.show_action_buttons
        )

    def answer(self, memory: int):
        sm = SMTwo(
            self.current_card.ease,
            (self.current_card.last_reviewed_at - datetime.now()).days,
            self.current_card.review_count,
        ).review(memory)
        if not sm.repetitions:
            self.cards.insert(0, self.current_card)
            self.current_card.next_review_after = datetime.now()
        else:
            self.current_card.next_review_after = sm.review_date
        self.current_card.last_reviewed_at = datetime.now()
        self.current_card.review_count = sm.repetitions
        self.current_card.ease = sm.easiness
        self.__repository.save()
        self.controller.notify_observers(
            CardAnswerObserver.EVENT_NAME,
            card=self.current_card,
            answer=int(memory),
            repeat_interval=sm.interval if sm.repetitions else 0,
        )
        if len(self.cards) == 0:
            self.end_game()
            return
        self.current_card = self.cards.pop()
        self.show_card()

    def load_data(self, group_id: int, **kwargs) -> None:
        self.cards = self.__repository.get_cards_to_study_by_group_id(group_id)
        if len(self.cards) == 0:
            self.end_game()
            return
        self.current_card = self.cards.pop()
        self.show_card()

    def show_card(self):
        self.front_text["text"] = self.current_card.front_text
        self.back_text["text"] = ""
        self.hide_action_buttons()

    def cards_count_changed(self):
        if len(self.cards) == 0:
            self.end_game()

    def end_game(self):
        self.controller.show_card_group()

    def show_action_buttons(self):
        self.again_button.pack()
        self.bad_button.pack()
        self.good_button.pack()
        self.easy_button.pack()
        self.perfect_button.pack()
        self.back_text["text"] = self.current_card.back_text
        self.show_answer_button.pack_forget()

    def hide_action_buttons(self):
        self.again_button.pack_forget()
        self.bad_button.pack_forget()
        self.good_button.pack_forget()
        self.easy_button.pack_forget()
        self.perfect_button.pack_forget()
        self.show_answer_button.pack()
