import tkinter as tk


class ImageCropper:
    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._is_activated = False
        self._rectangle = None
        self._rectangle_border_color = "red"
        self._rectangle_start_x = 0
        self._rectangle_start_y = 0
        self._rectangle_dx = 0
        self._rectangle_dy = 0
        self._setup()

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

    def _setup(self):
        self._canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self._canvas.bind("<B1-Motion>", self._on_mouse_move)

    def _on_mouse_press(self, event):
        if not self._is_activated:
            return

        if self._rectangle:
            self._canvas.delete(self._rectangle)

        self._rectangle_start_x = self._canvas.canvasx(event.x)
        self._rectangle_start_y = self._canvas.canvasx(event.y)

        self._rectangle = self._canvas.create_rectangle(
                self._rectangle_start_x, self._rectangle_start_y, 
                self._rectangle_start_x + 1, self._rectangle_start_y + 1, 
                outline = self._rectangle_border_color)

    def _on_mouse_move(self, event):
        if not self._is_activated or not self._rectangle:
            return

        self._rectangle_dx = self._canvas.canvasx(event.x)
        self._rectangle_dy = self._canvas.canvasy(event.y)

        self._canvas.coords(
                self._rectangle, 
                self._rectangle_start_x, self._rectangle_start_y, 
                self._rectangle_dx, self._rectangle_dy)

    def clear_selection(self):
        self._rectangle_start_x = 0
        self._rectangle_start_y = 0
        self._rectangle_dx = 0
        self._rectangle_dy = 0

        if self._rectangle:
            self._canvas.delete(self._rectangle)
            self._rectangle = None

