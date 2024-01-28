import tkinter as tk
from abc import ABC


class BasePage(ABC, tk.Frame):
    def load_data(self, **kwargs) -> None:
        pass
