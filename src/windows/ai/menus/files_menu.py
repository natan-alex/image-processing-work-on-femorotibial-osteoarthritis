import tkinter as tk

from globals import events


class FilesMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(label="Ler diretório", command=self._open_dir)

    def _open_dir(self):
        events.read_model_main_directory_button_clicked.emit()
