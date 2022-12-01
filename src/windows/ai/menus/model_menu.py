import tkinter as tk

from globals import events


class ModelMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(label="Treinar rede neural convolucional", command=self._train_model)

    def _train_model(self):
        events.train_neural_network_button_clicked.emit()
