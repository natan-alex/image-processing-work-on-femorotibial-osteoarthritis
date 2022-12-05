import tkinter as tk

from globals import events


class SelectionMenu(tk.Menu):
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
            label="Visualizar imagem da seleção",
            command=self._on_show_cropped_image_button_click)

        self.add_command(
            label="Salvar imagem da seleção",
            command=self._on_save_cropped_image_button_click)

        self.add_command(
            label="Sair do modo de seleção",
            command=self._on_leave_selection_mode_button_click)

    def _on_select_area_button_click(self):
        events.enter_selection_mode_button_clicked.emit()

    def _on_clear_selection_button_click(self):
        events.clear_selection_button_clicked.emit()

    def _on_leave_selection_mode_button_click(self):
        events.leave_selection_mode_button_clicked.emit()

    def _on_show_cropped_image_button_click(self):
        events.show_cropped_image_button_clicked.emit()

    def _on_save_cropped_image_button_click(self):
        events.save_cropped_image_button_clicked.emit()
