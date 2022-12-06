import tkinter as tk

from globals import events


class ModelMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(label="Carregar rede neural convolucional salva", command=self._load_nn)
        self.add_command(label="Treinar rede neural convolucional", command=self._train_nn)
        self.add_command(label="Treinar classificador raso", command=self._train_shallow_classifier)
        self.add_command(label="Treinar classificador xgboost", command=self._train_xgboost)
        self.add_command(label="Avaliar rede neural convolucional", command=self._evaluate_nn)
        self.add_command(label="Avaliar classificador raso", command=self._evaluate_shallow_classifier)
        self.add_command(label="Avaliar classificador xgboost", command=self._evaluate_xgboost)

    def _train_nn(self):
        events.train_neural_network_button_clicked.emit()

    def _train_xgboost(self):
        events.train_xgboost_classifier_button_clicked.emit()

    def _train_shallow_classifier(self):
        events.train_shallow_classifier_button_clicked.emit()

    def _load_nn(self):
        events.load_neural_network_button_clicked.emit()

    def _evaluate_nn(self):
        events.evaluate_neural_network_button_clicked.emit()

    def _evaluate_xgboost(self):
        events.evaluate_xgboost_button_clicked.emit()

    def _evaluate_shallow_classifier(self):
        events.evaluate_shallow_classifier_button_clicked.emit()
