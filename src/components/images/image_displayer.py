import tkinter as tk
from PIL import Image, ImageTk

from components.images.image_cropper import ImageCropper

from configs import APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT

from events.events import (
    file_selected_event, FileSelectedEventInfos,
    clear_image_button_clicked,
    clear_selection_button_clicked,
    select_area_button_clicked,
    crop_image_button_clicked,
)


class ImageDisplayer(tk.Canvas):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent, width = APP_DEFAULT_WIDTH, height = APP_DEFAULT_HEIGHT)
        self._canvas_width = APP_DEFAULT_WIDTH
        self._canvas_height = APP_DEFAULT_HEIGHT
        self._cropper = ImageCropper(self)
        self._text_wrapper = None
        self._image_wrapper = None
        self._image = None
        self._photo_image = None
        self._setup()

    def _set_text_wrapper(self):
        self._text_wrapper = self.create_text(
            self._canvas_width / 2, 
            self._canvas_height / 2, 
            text = "Nenhuma imagem selecionada")

    def _set_image_wrapper(self):
        self._image_wrapper = self.create_image(
            self._canvas_width / 2, 
            self._canvas_height / 2, 
            image = self._photo_image)

    def _setup(self):
        self._set_text_wrapper()
        self.pack(fill = tk.BOTH, anchor = tk.NW)

        file_selected_event.subscribe(self._on_file_selected)
        clear_image_button_clicked.subscribe(self._on_clear_image_button_click)
        clear_selection_button_clicked.subscribe(self._on_clear_selection_button_click)
        select_area_button_clicked.subscribe(self._on_select_area_button_click)
        crop_image_button_clicked.subscribe(self._on_crop_image_button_click)

    def _on_file_selected(self, event_infos: FileSelectedEventInfos):
        if self._text_wrapper:
            self.delete(self._text_wrapper)

        self._image = Image.open(event_infos.selected_file)
        self._photo_image = ImageTk.PhotoImage(self._image)
        self._set_image_wrapper()

    def _on_clear_image_button_click(self):
        if self._image_wrapper:
            self.delete(self._image_wrapper)

        self._image = None
        self._photo_image = None

        self._cropper.clear_selection()
        self._cropper.deactivate()

    def _on_clear_selection_button_click(self):
        self._cropper.clear_selection()

    def _on_select_area_button_click(self):
        if self._image:
            self._cropper.activate()

    def _on_crop_image_button_click(self):
        if not self._cropper.is_activated: return
        if not self._cropper.has_selection: return
        if not self._image: return
        coordinates = self._cropper.selection_coordinates
        if not coordinates: return
        print('coords: ', coordinates)
        self._image = self._image.crop(coordinates)
        self._image.show()

