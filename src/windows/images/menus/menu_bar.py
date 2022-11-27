import tkinter as tk

from globals import events

from windows.images.menus.selection_menu import SelectionMenu


class MenuBar(tk.Menu):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Selecionar imagem",
            command=self._open_file_explorer)

        self.add_command(
            label="Remover imagem selecionada",
            command=self._clear_selected_image)

    def _add_submenus(self):
        self.add_cascade(label="Seleção", menu=SelectionMenu(self))

    def _open_file_explorer(self):
        events.select_image_button_clicked.emit()

    def _clear_selected_image(self):
        events.clear_image_button_clicked.emit()
