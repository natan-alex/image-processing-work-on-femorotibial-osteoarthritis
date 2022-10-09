import tkinter as tk
import configs
from components.menubar import MenuBar
from components.images.image_displayer import ImageDisplayer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._menubar = MenuBar(self)
        self._image_displayer = ImageDisplayer(self)
        self._setup()

    def _setup(self):
        height = configs.app_default_height
        width = configs.app_default_width
        self.geometry(f"{width}x{height}")
        self.config(menu = self._menubar)
