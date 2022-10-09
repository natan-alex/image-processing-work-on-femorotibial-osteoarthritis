import tkinter as tk
from configs import APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT
from components.menubar import MenuBar
from components.images.image_displayer import ImageDisplayer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._menubar = MenuBar(self)
        self._image_displayer = ImageDisplayer(self)
        self._setup()

    def _setup(self):
        height = APP_DEFAULT_HEIGHT
        width = APP_DEFAULT_WIDTH
        self.geometry(f"{width}x{height}")
        self.config(menu = self._menubar)
