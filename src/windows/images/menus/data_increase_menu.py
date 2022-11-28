import tkinter as tk

from globals import events


class DataIncreaseMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Equalização de histograma",
            command=self._on_histogram_equalization_button_click)

        self.add_command(
            label="Espelhamento horizontal",
            command=self._on_horizontal_mirroring_button_click)

    def _on_histogram_equalization_button_click(self):
        events.histogram_equalization_button_clicked.emit()

    def _on_horizontal_mirroring_button_click(self):
        events.horizontal_mirroring_button_clicked.emit()
