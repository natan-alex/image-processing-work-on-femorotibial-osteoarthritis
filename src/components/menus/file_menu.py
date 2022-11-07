import tkinter as tk

from events.events import (
    select_image_button_clicked,
    clear_image_button_clicked,
    save_cropped_image_button_clicked,
    show_cropped_image_button_clicked,
)


class FileMenu(tk.Menu):
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
            label="Visualizar imagem do recorte",
            command=self._on_show_cropped_image_button_click)

        self.add_command(
            label="Salvar imagem do recorte",
            command=self._on_save_cropped_image_button_click)

        self.add_command(
            label="Remover imagem selecionada",
            command=self._clear_selected_image)

    def _open_file_explorer(self):
        select_image_button_clicked.emit()

    def _clear_selected_image(self):
        clear_image_button_clicked.emit()

    def _on_show_cropped_image_button_click(self):
        show_cropped_image_button_clicked.emit()

    def _on_save_cropped_image_button_click(self):
        save_cropped_image_button_clicked.emit()
