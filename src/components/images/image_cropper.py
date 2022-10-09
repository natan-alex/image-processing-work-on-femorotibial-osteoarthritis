import tkinter as tk
from typing import Tuple, Union


class ImageCropper:
    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._is_activated = False
        self._rectangle = None
        self._rectangle_border_color = "red"
        self._start_x = 0
        self._start_y = 0
        self._end_x = 0
        self._end_y = 0
        self._setup()

    def _setup(self):
        self._canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self._canvas.bind("<B1-Motion>", self._on_mouse_move)
        self._canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

    def _adjust_rectangle_state(self):
        if self._rectangle:
            state = "normal" if self._is_activated else "hidden"
            self._canvas.itemconfigure(self._rectangle, state = state)

    def activate(self):
        self._is_activated = True
        self._adjust_rectangle_state()
        self._canvas.configure(cursor = "cross")

    def deactivate(self):
        self._is_activated = False
        self._adjust_rectangle_state()
        self._canvas.configure(cursor = "")

    def _on_mouse_press(self, event):
        if not self._is_activated: return

        if self._rectangle:
            self._canvas.delete(self._rectangle)
            self._rectangle = None

        self._start_x = self._canvas.canvasx(event.x)
        self._start_y = self._canvas.canvasx(event.y)

        print('event x: ', event.y)
        print('event y: ', event.x)
        print('start x: ', self._start_x)
        print('start y: ', self._start_y)

    def _on_mouse_move(self, event):
        if not self._is_activated: return

        if not self._rectangle:
            self._rectangle = self._canvas.create_rectangle(
                self._start_x, self._start_y, 
                self._start_x + 1, self._start_y + 1,
                outline = self._rectangle_border_color)

        self._end_x = self._canvas.canvasx(event.x)
        self._end_y = self._canvas.canvasy(event.y)

        self._canvas.coords(
            self._rectangle, 
            self._start_x, self._start_y, 
            self._end_x, self._end_y)

    def _on_mouse_release(self, event):
        if not self._is_activated: return

        self._end_x = self._canvas.canvasx(event.x)
        self._end_y = self._canvas.canvasy(event.y)

        print('event x: ', event.y)
        print('event y: ', event.x)
        print('end x: ', self._end_x)
        print('end y: ', self._end_y)

    def clear_selection(self):
        self._start_x = 0
        self._start_y = 0

        if self._rectangle:
            self._canvas.delete(self._rectangle)
            self._rectangle = None

    @property
    def is_activated(self) -> bool:
        return self._is_activated

    @property
    def has_selection(self) -> bool:
        return self._rectangle != None

    @property
    def selection_coordinates(self) -> Union[Tuple[int, int, int, int], None]:
        if not self.has_selection:
            return None

        left = self._start_x
        upper = self._start_y
        right = self._end_x
        lower = self._end_y

        return (left, upper, right, lower)
