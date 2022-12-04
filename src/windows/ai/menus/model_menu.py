import tkinter as tk

from globals import events


class ModelMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(label="Carregar modelo salvo", command=self._load_saved_model)
        self.add_command(label="Treinar rede neural convolucional", command=self._train_nn)
        self.add_command(label="Avaliar rede neural convolucional", command=self._evaluate_nn)

    def _train_nn(self):
        events.train_neural_network_button_clicked.emit()

    def _load_saved_model(self):
        events.load_saved_model_button_clicked.emit()

    def _evaluate_nn(self):
        events.evaluate_neural_network_button_clicked.emit()
