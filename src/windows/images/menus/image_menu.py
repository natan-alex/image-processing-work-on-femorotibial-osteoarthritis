import tkinter as tk

from globals import events


class ImageMenu(tk.Menu):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Encontrar correlação cruzada com outra imagem",
            command=self._find_cross_correlation_button_click)

    def _find_cross_correlation_button_click(self):
        events.find_cross_correlation_button_clicked.emit()
