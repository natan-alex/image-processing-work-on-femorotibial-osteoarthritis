import tkinter as tk

from configs import WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        self.resizable(False, False)
        self.update()
