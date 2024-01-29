import tkinter as tk
from src.Repository.CardRepository import CardRepository
from src.Entity.Card import Card
from .BasePage import BasePage
from src.Observer.CardAnswerObserver import CardAnswerObserver


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

        self.dont_remember_button = tk.Button(
            self, text="Bad", command=lambda: self.answer(False)
        )

        self.good_remember_button = tk.Button(
            self, text="Good", command=lambda: self.answer(True)
        )

        self.show_answer_button = tk.Button(
            self, text="Show Answer", command=self.show_action_buttons
        )

    def answer(self, memory: bool):
        self.controller.notify_observers(
            CardAnswerObserver.EVENT_NAME, card=self.current_card, answer=int(memory)
        )
        if memory:
            self.current_card.reviewed()
            self.__repository.save()
            if len(self.cards) == 0:
                self.end_game()
                return
        else:
            self.cards.insert(0, self.current_card)
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
        self.dont_remember_button.pack(side=tk.LEFT)
        self.good_remember_button.pack(side=tk.RIGHT)
        self.back_text["text"] = self.current_card.back_text
        self.show_answer_button.pack_forget()

    def hide_action_buttons(self):
        self.dont_remember_button.pack_forget()
        self.good_remember_button.pack_forget()
        self.show_answer_button.pack()
