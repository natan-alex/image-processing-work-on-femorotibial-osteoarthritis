import tkinter as tk

from events.events import (
    train_model_button_clicked
)


class IaRelatedMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Treinar modelo",
            command=self._on_train_model_button_click)

    def _on_train_model_button_click(self):
        train_model_button_clicked.emit()
