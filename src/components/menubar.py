import tkinter as tk
from components.menus import file_menu


class MenuBar(tk.Menu):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self._file_menu = file_menu.FileMenu(self)
        self._setup()

    def _setup(self):
        self.add_cascade(
            label="Arquivos",
            menu=self._file_menu
        )

    @property
    def file_menu(self) -> file_menu.FileMenu:
        return self._file_menu
