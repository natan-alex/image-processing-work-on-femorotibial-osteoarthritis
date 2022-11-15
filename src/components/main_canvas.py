import tkinter as tk
from typing import Tuple
from PIL.Image import Image


class MainCanvas(tk.Canvas):
    def __init__(self, window: tk.Tk):
        super().__init__(
            window,
            width=window.winfo_width(),
            height=window.winfo_height(),
            borderwidth=0,
            highlightthickness=0)

        self.pack(fill=tk.BOTH, anchor=tk.NW, padx=0, pady=0)
        self.update()

    def get_margins_for(self, image: Image) -> Tuple[int, int]:
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        width, height = image.size

        margin_left = (canvas_width - width) / 2
        margin_top = (canvas_height - height) / 2

        return (margin_left, margin_top)
