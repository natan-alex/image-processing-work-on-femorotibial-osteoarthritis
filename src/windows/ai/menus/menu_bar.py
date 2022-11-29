import tkinter as tk

from globals import events

class MenuBar(tk.Menu):
    """ 
    The menu bar for the ai window. 
    Agregate submenus in a single bar
    """

    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self._add_menu_items()

    def _add_menu_items(self):
        self.add_command(
            label="Ler diretório",
            command=self._open_dir)

    def _open_dir(self):
        events.read_model_main_directory_button_clicked.emit()
