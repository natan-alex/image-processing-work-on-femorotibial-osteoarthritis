import tkinter as tk

from events.events import (
    clear_selection_button_clicked,
    select_area_button_clicked,
    crop_image_button_clicked,
)


class InteractionsMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff = False)
        self._setup()

    def _setup(self):
        self.add_command(
            label = "Selecionar área", 
            command = self._on_select_area_button_click)

        self.add_command(
            label = "Remover seleção de área", 
            command = self._on_clear_selection_button_click)

        self.add_command(
            label = "Recortar imagem da seleção", 
            command = self._on_crop_image_button_click)

    def _on_select_area_button_click(self):
        select_area_button_clicked.emit()

    def _on_clear_selection_button_click(self):
        clear_selection_button_clicked.emit()

    def _on_crop_image_button_click(self):
        crop_image_button_clicked.emit()
