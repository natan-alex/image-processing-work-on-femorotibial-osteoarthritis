import tkinter as tk
from components import menubar, image_displayer


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._menubar = menubar.MenuBar(self)
        self._image_displayer = image_displayer.ImageDisplayer(self)
        self._setup()

    def _setup(self):
        self.geometry("800x600")
        self.config(menu=self._menubar)
