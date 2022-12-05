import tkinter as tk

from globals import events


class ImageMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Selecionar imagem",
            command=self._open_file_explorer)

        self.add_command(
            label="Remover imagem selecionada",
            command=self._clear_selected_image)

    def _open_file_explorer(self):
        events.select_image_button_clicked.emit()

    def _clear_selected_image(self):
        events.clear_image_button_clicked.emit()
