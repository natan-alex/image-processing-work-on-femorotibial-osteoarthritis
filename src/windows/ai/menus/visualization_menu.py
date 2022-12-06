import tkinter as tk

from globals import events


class VisualizationMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Plotar matriz de confusão para a rede neural convolucional",
            command=self._plot_confusion_matrix_for_nn)

        self.add_command(
            label="Plotar matriz de confusão para o classificador raso",
            command=self._plot_confusion_matrix_for_shallow_classifier)

        self.add_command(
            label="Plotar matriz de confusão para o xgboost",
            command=self._plot_confusion_matrix_for_xgboost)

    def _plot_confusion_matrix_for_nn(self):
        events.plot_confusion_matrix_for_neural_network_button_clicked.emit()

    def _plot_confusion_matrix_for_xgboost(self):
        events.plot_confusion_matrix_for_xgboost_button_clicked.emit()

    def _plot_confusion_matrix_for_shallow_classifier(self):
        events.plot_confusion_matrix_for_shallow_classifier_button_clicked.emit()
