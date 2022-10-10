import tkinter as tk
from PIL import ImageTk

from events.events import *
from components.images.util import ImageUtil, ImageOpenBuilder
from components.images.image_cropper import ImageCropper
from configs import APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT


class ImageDisplayer(tk.Canvas):
    def __init__(self, parent: tk.Tk):
        super().__init__(
            parent,
            width=APP_DEFAULT_WIDTH,
            height=APP_DEFAULT_HEIGHT,
            borderwidth=0,
            highlightthickness=0)

        self._canvas_width = APP_DEFAULT_WIDTH
        self._canvas_height = APP_DEFAULT_HEIGHT
        self._cropper = ImageCropper(self)
        self._text_container = None
        self._image_container = None
        self._image = None
        self._photo_image = None
        self._cropped_image = None
        self._setup()

    def _create_text_container(self, text="Nenhuma imagem selecionada"):
        self._text_container = self.create_text(
            self._canvas_width / 2,
            self._canvas_height / 2,
            text=text)

    def _create_image_container(self):
        if self._photo_image is None:
            return

        self._image_container = self.create_image(
            self._canvas_width / 2,
            self._canvas_height / 2,
            image=self._photo_image)

    def _setup(self):
        self._create_text_container()
        self.pack(fill=tk.BOTH, anchor=tk.NW, padx=0, pady=0)

        select_image_button_clicked.subscribe(
            self._on_select_image_button_click)
        clear_image_button_clicked.subscribe(
            self._on_clear_image_button_click)
        clear_selection_button_clicked.subscribe(
            self._on_clear_selection_button_click)
        enter_selection_mode_button_clicked.subscribe(
            self._on_enter_selection_mode_button_click)
        leave_selection_mode_button_clicked.subscribe(
            self._on_leave_selection_mode_button_click)
        show_cropped_image_button_clicked.subscribe(
            self._on_show_cropped_image_button_click)
        area_selection_finished.subscribe(
            self._on_area_selection_finished)
        save_cropped_image_button_clicked.subscribe(
            self._on_save_cropped_image_button_click)

    def _on_select_image_button_click(self):
        image = (
            ImageOpenBuilder()
            .select()
            .then_open()
            .then_resize_to(self.winfo_width(), self.winfo_height())
            .then_get_result()
        )

        if image is None:
            return

        if self._text_container:
            self.delete(self._text_container)

        self._image = image
        self._photo_image = ImageTk.PhotoImage(self._image)
        self._create_image_container()
        self._cropper.activate()
        self._cropper.set_selected_image(self._image)

    def _on_clear_image_button_click(self):
        if self._image_container:
            self.delete(self._image_container)

        self._image = None
        self._photo_image = None
        self._cropped_image = None
        self._cropper.deactivate()
        self._create_text_container()

    def _on_clear_selection_button_click(self):
        self._cropper.clear_selection()
        self._cropped_image = None

    def _on_enter_selection_mode_button_click(self):
        if self._image:
            self._cropper.activate()

    def _on_leave_selection_mode_button_click(self):
        self._cropper.deactivate()
        self._cropped_image = None

    def _on_area_selection_finished(
        self,
        event: AreaSelectionFinishedEventInfos
    ):
        if not self._cropper.is_activated:
            return
        if not self._cropper.has_selection:
            return
        if self._image is None:
            return

        self._cropped_image = event.cropped_image

    def _on_show_cropped_image_button_click(self):
        if self._cropped_image is None:
            return

        self._cropped_image.show()

    def _on_save_cropped_image_button_click(self):
        if self._cropped_image is None:
            return

        ImageUtil.save(self._cropped_image)
