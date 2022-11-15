import tkinter as tk

from configs import APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{APP_DEFAULT_WIDTH}x{APP_DEFAULT_HEIGHT}")
        self.resizable(False, False)
        self.update()
