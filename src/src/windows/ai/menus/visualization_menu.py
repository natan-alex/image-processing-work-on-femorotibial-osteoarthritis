import tkinter as tk

from globals import events


class VisualizationMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Plotar matriz de confusão",
            command=self._plot_confusion_matrix)

    def _plot_confusion_matrix(self):
        events.plot_confusion_matrix_button_clicked.emit()

