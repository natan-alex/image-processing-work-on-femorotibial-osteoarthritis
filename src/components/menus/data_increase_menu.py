import tkinter as tk

from events.events import (
    equalize_histogram_button_clicked
)


class DataIncreaseMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Equalização de histograma",
            command=self._on_equalize_histogram_click)

    def _on_equalize_histogram_click(self):
        equalize_histogram_button_clicked.emit()
