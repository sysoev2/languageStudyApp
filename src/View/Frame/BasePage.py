import tkinter as tk
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from index.main import TkinterApp
else:
    TkinterApp = "TkinterApp"


class BasePage(ABC, tk.Frame):
    controller: TkinterApp

    def __init__(self, parent, controller: TkinterApp):
        self.controller = controller
        super().__init__(parent)

    def load_data(self, **kwargs) -> None:
        pass
