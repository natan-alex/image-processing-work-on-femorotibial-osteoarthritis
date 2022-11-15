import tkinter as tk

from events.events import (
    select_image_button_clicked,
    clear_image_button_clicked,
    find_cross_correlation_button_clicked,
)


class ImageMenu(tk.Menu):
    """
    Class that contains options for files related tab
    Emits an event when an option is selected
    """

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

        self.add_command(
            label="Encontrar correlação cruzada com outra imagem",
            command=self._find_cross_correlation_button_click)

    def _open_file_explorer(self):
        select_image_button_clicked.emit()

    def _clear_selected_image(self):
        clear_image_button_clicked.emit()

    def _find_cross_correlation_button_click(self):
        find_cross_correlation_button_clicked.emit()
