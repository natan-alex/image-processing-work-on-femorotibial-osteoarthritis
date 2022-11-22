import tkinter as tk

from configs import WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT
from components.canvas.main_canvas import MainCanvas
from components.menus.menu_bar import MenuBar
from components.aside.aside_box import AsideBox


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        self.resizable(False, False)
        self.update()

        self._add_components()

    def _add_components(self):
        self._add_menu_bar()
        self._add_main_canvas()
        self._add_aside_box()

    def _add_menu_bar(self):
        self._menu_bar = MenuBar(self)
        self.config(menu=self._menu_bar)
        self.update()

    def _add_main_canvas(self):
        self._canvas_frame = tk.Frame(self, width=self.winfo_width() * 0.7)
        self._canvas_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.update()
        self._main_canvas = MainCanvas(self._canvas_frame)
        self._main_canvas.pack()
        self.update()

    def _add_aside_box(self):
        self._aside_box_frame = tk.Frame(self, width=self.winfo_width() * 0.3)
        self._aside_box_frame.pack(fill=tk.Y, side=tk.RIGHT)
        self.update()
        self._aside_box = AsideBox(self._aside_box_frame)
        self._aside_box.pack()
        self.update()

    @property
    def main_canvas(self) -> MainCanvas:
        return self._main_canvas

    @property
    def aside_box(self) -> AsideBox:
        return self._aside_box
