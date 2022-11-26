import tkinter as tk

from events.events import (
    read_model_main_directory_button_clicked
)


class AiRelatedMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Ler diretório principal",
            command=self._on_read_main_directory_button_click)

    def _on_read_main_directory_button_click(self):
        read_model_main_directory_button_clicked.emit()
