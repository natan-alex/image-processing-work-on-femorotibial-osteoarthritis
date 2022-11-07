import tkinter as tk

from events.events import (
    clear_selection_button_clicked,
    enter_selection_mode_button_clicked,
    leave_selection_mode_button_clicked,
    find_cross_correlation_button_clicked,
)


class InteractionsMenu(tk.Menu):
    """
    Class that contains options for interactions related tab
    Emits an event when an option is selected
    """

    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff=False)
        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Entrar no modo de seleção",
            command=self._on_select_area_button_click)

        self.add_command(
            label="Remover seleção de área",
            command=self._on_clear_selection_button_click)

        self.add_command(
            label="Sair do modo de seleção",
            command=self._on_leave_selection_mode_button_click)

        self.add_command(
            label="Encontrar correlação cruzada",
            command=self._find_cross_correlation_button_click)

    def _on_select_area_button_click(self):
        enter_selection_mode_button_clicked.emit()

    def _on_clear_selection_button_click(self):
        clear_selection_button_clicked.emit()

    def _on_leave_selection_mode_button_click(self):
        leave_selection_mode_button_clicked.emit()

    def _find_cross_correlation_button_click(self):
        find_cross_correlation_button_clicked.emit()
