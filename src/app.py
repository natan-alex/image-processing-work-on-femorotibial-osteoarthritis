import tkinter as tk
from configs import APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT
from components.menus.menubar import MenuBar
from components.displayer import Displayer


class App(tk.Tk):
    """
    The class that represents the hole application
    Join all components in one place
    """

    def __init__(self):
        super().__init__()
        self._menubar = MenuBar(self)
        self._displayer = Displayer(self)
        self._setup()

    def _setup(self):
        height = APP_DEFAULT_HEIGHT
        width = APP_DEFAULT_WIDTH
        self.geometry(f"{width}x{height}")
        self.config(menu=self._menubar)
        self.resizable(False, False)
