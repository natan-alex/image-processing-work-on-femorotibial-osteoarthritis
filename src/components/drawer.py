import tkinter as tk
from PIL import Image
from typing import Tuple

from events.events import (
    area_selection_finished, AreaSelectionFinishedEventInfos
)


class Drawer:
    """
    Class that can draw rectangles in the main screen
    and crop the selected image in the corresponding
    area
    """

    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._selected_image = None
        self._is_activated = False
        self._rectangle = None
        self._image_margin_left = 0
        self._image_margin_top = 0
        self._rectangle_start_x = 0
        self._rectangle_start_y = 0
        self._rectangle_end_x = 0
        self._rectangle_end_y = 0
        self._setup()

    def _setup(self):
        """
        Bind mouse events to the corresponding listeners
        """

        self._canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self._canvas.bind("<B1-Motion>", self._on_mouse_move)
        self._canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

    def _delete_rectangle(self):
        """
        Delete the rectangle selection if it exists
        """

        if self._rectangle is not None:
            self._canvas.delete(self._rectangle)
            self._rectangle = None

    def set_selected_image(self, image: Image):
        """
        Set the selected image that corresponds to
        the image that is being shown in the screen
        Also store the margins that it takes if its
        smaller than the canvas size for adjust the
        cropping coordinates
        """

        self._selected_image = image

        self._delete_rectangle()

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        image_width, image_height = image.size

        self._image_margin_left = (canvas_width - image_width) / 2
        self._image_margin_top = (canvas_height - image_height) / 2

    def activate(self):
        """
        Allow user to draw something with the mouse
        """

        self._is_activated = True
        self._canvas.configure(cursor="cross")

    def deactivate(self):
        """
        Do not allow user to draw something with the mouse
        """

        self._is_activated = False
        self._delete_rectangle()
        self._selected_image = None
        self._canvas.configure(cursor="")

    def _create_rectangle_if_not_exist(self):
        """
        Create a small rectangle on the canvas if
        there is no rectangle yet
        """

        if self._rectangle is None:
            self._rectangle = self._canvas.create_rectangle(
                self._rectangle_start_x, self._rectangle_start_y,
                self._rectangle_start_x + 1, self._rectangle_start_y + 1,
                outline="red")

    def _move_rectangle_coordinates(self):
        """
        Moves the rectangle based on start_x, start_y,
        end_x and end_y values
        """

        if self._rectangle is not None:
            self._canvas.coords(
                self._rectangle,
                self._rectangle_start_x, self._rectangle_start_y,
                self._rectangle_end_x, self._rectangle_end_y)

    def _on_mouse_press(self, event):
        """
        Catch the event and set start_x and start_y
        variables with where the click happened
        It deletes the previous rectangle to avoid
        conflicts
        """

        if not self._is_activated:
            return

        self._delete_rectangle()

        self._rectangle_start_x = self._canvas.canvasx(event.x)
        self._rectangle_start_y = self._canvas.canvasx(event.y)

    def _on_mouse_move(self, event):
        """
        Catch the mouse move event and set end_x and end_y
        variables with where the mouse is going
        """

        if not self._is_activated:
            return

        self._create_rectangle_if_not_exist()

        self._rectangle_end_x = self._canvas.canvasx(event.x)
        self._rectangle_end_y = self._canvas.canvasy(event.y)

        self._move_rectangle_coordinates()

    def _on_mouse_release(self, event):
        """
        Catch the event and set end_x and end_y
        variables with where the mouse stopped
        Emit the corresponding event with the
        cropped image based on the selected area
        """

        if self._selected_image is None:
            return

        coordinates = (
            self._rectangle_start_x - self._image_margin_left,
            self._rectangle_start_y - self._image_margin_top,
            self._rectangle_end_x - self._image_margin_left,
            self._rectangle_end_y - self._image_margin_top,
        )

        cropped_image = self._selected_image.crop(coordinates)
        event_infos = AreaSelectionFinishedEventInfos(cropped_image)
        area_selection_finished.emit(event_infos)

    def draw_rectangle_considering_image_margins(
        self,
        start_point: Tuple[int, int],
        end_point: Tuple[int, int]
    ):
        """
        Draw a rectangle considering the margins
        that the image can have if it is smaller
        than the canvas size
        """

        if self._selected_image is None:
            return

        self._delete_rectangle()

        self._rectangle = self._canvas.create_rectangle(
            start_point[0] + self._image_margin_left,
            start_point[1] + self._image_margin_top,
            end_point[0] + self._image_margin_left,
            end_point[1] + self._image_margin_top,
            outline="blue"
        )

    def clear_selection(self):
        self._delete_rectangle()

    @property
    def is_activated(self) -> bool:
        return self._is_activated

    @property
    def has_selection(self) -> bool:
        return self._rectangle is not None
