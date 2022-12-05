import tkinter as tk
from typing import Tuple

from globals.events import (
    rectangle_finished_drawing, RectangleFinishedDrawingEventInfos
)


class RectangleDrawer:
    """
    A class for drawing rectangles on a canvas 
    with the mouse movements
    """

    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._is_activated = False
        self._rectangle = None
        self._start_x = 0
        self._start_y = 0
        self._end_x = 0
        self._end_y = 0

        self._setup()

    def _setup(self):
        self._canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self._canvas.bind("<B1-Motion>", self._on_mouse_move)
        self._canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

    def delete_rectangle(self):
        """
        Delete the rectangle selection if it exists
        """

        if self._rectangle is not None:
            self._canvas.delete(self._rectangle)
            self._rectangle = None

    def _create_rectangle(self):
        """
        Create a small rectangle on the canvas if
        there is no rectangle yet
        """

        if self._rectangle is None:
            self._rectangle = self._canvas.create_rectangle(
                self._start_x, self._start_y,
                self._start_x, self._start_y,
                outline="red")

    def _move_rectangle_coordinates(self):
        """
        Moves the rectangle based on start_x, start_y,
        end_x and end_y values
        """

        if self._rectangle is not None:
            self._canvas.coords(
                self._rectangle,
                self._start_x, self._start_y,
                self._end_x, self._end_y)

    def _on_mouse_press(self, event):
        """
        Catch the event and set start_x and start_y
        variables with where the click happened
        It deletes the previous rectangle
        """

        if not self._is_activated:
            return

        self.delete_rectangle()

        self._start_x = self._canvas.canvasx(event.x)
        self._start_y = self._canvas.canvasx(event.y)

    def _on_mouse_move(self, event):
        """
        Catch the mouse move event and set end_x and end_y
        variables with where the mouse is going
        """

        if not self._is_activated:
            return

        self._create_rectangle()

        self._end_x = self._canvas.canvasx(event.x)
        self._end_y = self._canvas.canvasy(event.y)

        self._move_rectangle_coordinates()

    def _on_mouse_release(self, _):
        """
        Handle mouse release event. Computes the end 
        point of the rectangle and consider if it 
        was drawn from bottom to up or the reverse
        """

        if not self._is_activated:
            return

        if self._start_x > self._end_x:
            self._start_x, self._end_x = self._end_x, self._start_x

        if self._start_y > self._end_y:
            self._start_y, self._end_y = self._end_y, self._start_y

        infos = RectangleFinishedDrawingEventInfos(
            start_point=(self._start_x, self._start_y),
            end_point=(self._end_x, self._end_y))

        rectangle_finished_drawing.emit(infos)

    def activate(self):
        self._is_activated = True
        self._canvas.configure(cursor="cross")

    def deactivate(self):
        self._is_activated = False
        self._canvas.configure(cursor="")

    def draw_rectangle(
        self,
        start_point: Tuple[int, int],
        end_point: Tuple[int, int]
    ):
        """ Get the rectangle coordinates and draw it """

        self.delete_rectangle()

        self._rectangle = self._canvas.create_rectangle(
            start_point[0], start_point[1],
            end_point[0], end_point[1],
            outline="blue")
