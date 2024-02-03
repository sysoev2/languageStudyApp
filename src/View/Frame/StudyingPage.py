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

        # Action buttons using grid layout
        tk.Button(
            self.action_buttons_frame,
            text="Again",
            command=lambda: self.answer(CardComplexity.Again.value),
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            self.action_buttons_frame,
            text="Bad",
            command=lambda: self.answer(CardComplexity.Bad.value),
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            self.action_buttons_frame,
            text="Good",
            command=lambda: self.answer(CardComplexity.Good.value),
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            self.action_buttons_frame,
            text="Easy",
            command=lambda: self.answer(CardComplexity.Easy.value),
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            self.action_buttons_frame,
            text="Perfect",
            command=lambda: self.answer(CardComplexity.Perfect.value),
        ).grid(row=0, column=4, padx=5)

        # Frame for show answer button to align using grid
        self.show_answer_frame = tk.Frame(self.main_frame)
        self.show_answer_frame.grid(row=3, column=0, columnspan=5)

        self.show_answer_button = tk.Button(
            self.show_answer_frame, text="Show Answer", command=self.show_action_buttons
        )
        self.show_answer_button.pack()

        # Initially hide the action buttons frame
        self.action_buttons_frame.grid_remove()

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
        """Show the answer and action buttons, hide the 'Show Answer' button."""
        self.back_text["text"] = self.current_card.back_text
        self.show_answer_frame.grid_remove()  # Hide 'Show Answer' button frame
        self.action_buttons_frame.grid()  # Show action buttons frame

    def hide_action_buttons(self):
        """Hide the action buttons and show the 'Show Answer' button."""
        self.action_buttons_frame.grid_remove()  # Hide action buttons frame
        self.show_answer_frame.grid()  # Show 'Show
