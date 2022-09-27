import tkinter as tk
from components.menubar import MenuBar
from components.image_displayer import ImageDisplayer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Trabalho")
        self.update()
        print(f'root w: {self.winfo_width()}, h: {self.winfo_height()}')
        self._menubar = MenuBar(self)
        self._image_displayer = ImageDisplayer(self)
        self.config(menu=self._menubar)
