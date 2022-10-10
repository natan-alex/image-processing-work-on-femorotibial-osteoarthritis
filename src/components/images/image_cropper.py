import tkinter as tk
from PIL import Image

from events.events import (
    area_selection_finished, AreaSelectionFinishedEventInfos
)


class ImageCropper:
    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._selected_image = None
        self._is_activated = False
        self._rectangle = None
        self._rectangle_border_color = "red"
        self._image_margin_left = 0
        self._image_margin_top = 0
        self._start_x = 0
        self._start_y = 0
        self._end_x = 0
        self._end_y = 0
        self._setup()

    def _setup(self):
        self._canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self._canvas.bind("<B1-Motion>", self._on_mouse_move)
        self._canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

    def _delete_rectangle(self):
        if self._rectangle:
            self._canvas.delete(self._rectangle)
            self._rectangle = None

    def set_selected_image(self, image: Image):
        self._selected_image = image
        self._delete_rectangle()
        self._is_activated = False
        self._canvas.configure(cursor="")

        width_diff = self._canvas.winfo_width() - image.size[0]
        height_diff = self._canvas.winfo_height() - image.size[1]

        self._image_margin_left = width_diff / 2
        self._image_margin_top = height_diff / 2

    def activate(self):
        self._is_activated = True
        self._canvas.configure(cursor="cross")

    def deactivate(self):
        self._is_activated = False
        self._delete_rectangle()
        self._selected_image = None
        self._image_margin_left = 0
        self._image_margin_top = 0
        self._canvas.configure(cursor="")

    def _create_rectangle_if_not_exist(self):
        if self._rectangle is None:
            self._rectangle = self._canvas.create_rectangle(
                self._start_x, self._start_y,
                self._start_x + 1, self._start_y + 1,
                outline=self._rectangle_border_color)

    def _move_rectangle_coordinates(self):
        if self._rectangle:
            self._canvas.coords(
                self._rectangle,
                self._start_x, self._start_y,
                self._end_x, self._end_y)

    def _on_mouse_press(self, event):
        if not self._is_activated:
            return

        self._delete_rectangle()

        self._start_x = self._canvas.canvasx(event.x)
        self._start_y = self._canvas.canvasx(event.y)

    def _on_mouse_move(self, event):
        if not self._is_activated:
            return

        self._create_rectangle_if_not_exist()

        self._end_x = self._canvas.canvasx(event.x)
        self._end_y = self._canvas.canvasy(event.y)

        self._move_rectangle_coordinates()

    def _on_mouse_release(self, event):
        if self._selected_image is None:
            return

        coordinates = (
            self._start_x - self._image_margin_left,
            self._start_y - self._image_margin_top,
            self._end_x - self._image_margin_left,
            self._end_y - self._image_margin_top,
        )

        cropped_image = self._selected_image.crop(coordinates)
        event_infos = AreaSelectionFinishedEventInfos(cropped_image)
        area_selection_finished.emit(event_infos)

    def clear_selection(self):
        self._delete_rectangle()

    @property
    def is_activated(self) -> bool:
        return self._is_activated

    @property
    def has_selection(self) -> bool:
        return self._rectangle is not None
