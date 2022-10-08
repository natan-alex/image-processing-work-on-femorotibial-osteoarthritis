import tkinter as tk
from PIL import Image, ImageTk

import configs
from events.events import (
    file_selected_event, FileSelectedEventInfos,
    clear_image_button_clicked
)


class ImageDisplayer(tk.Canvas):
    def __init__(self, parent: tk.Tk):
        width = configs.app_default_width
        height = configs.app_default_height
        super().__init__(parent, width = width, height = height)
        self._image = None
        self._photo_image = None
        self._text_wrapper = self.create_text(width / 2, height / 2, text = "Nenhuma imagem selecionada")
        self._image_wrapper = self.create_image(width / 2, height / 2)
        self._setup()

    def _setup(self):
        self.pack(fill = tk.BOTH, anchor = tk.NW)
        file_selected_event.subscribe(self._on_file_selected)
        clear_image_button_clicked.subscribe(self._clear_selected_image)

    def _on_file_selected(self, event_infos: FileSelectedEventInfos):
        self.itemconfig(self._text_wrapper, text = None)

        self._image = Image.open(event_infos.selected_file)
        self._photo_image = ImageTk.PhotoImage(self._image)
        self.itemconfig(self._image_wrapper, image = self._photo_image)

    def _clear_selected_image(self, _):
        self.itemconfig(self._text_wrapper, text = "Nenhuma imagem selecionada")

        self._image = None
        self._photo_image = None
        self.itemconfig(self._image_wrapper, image = None)
