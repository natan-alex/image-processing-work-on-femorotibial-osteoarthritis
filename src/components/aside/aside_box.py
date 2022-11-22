import tkinter as tk


class AsideBox(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

        tk.Button(self, text="button").pack()
