import tkinter as tk
import tkinter.filedialog as tk_files

from events.events import (
    file_selected_event, FileSelectedEventInfos,
    clear_image_button_clicked,
)


class FileMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        super().__init__(parent, tearoff = False)
        self._setup()

    def _setup(self):
        self.add_command(label = "Selecionar", command = self._open_file_explorer)
        self.add_command(label = "Remover imagem", command = self._clear_selected_image)

    def _open_file_explorer(self):
        filetypes = [
            ("Imagens", "*.jpg *.png"),
            ("Todos os arquivos", "*.*")
        ]

        selected_file = tk_files.askopenfilename(
            initialdir="~",
            title="Escolha uma imagem",
            filetypes=filetypes
        )
        
        if selected_file:
            file_selected_event.emit(FileSelectedEventInfos(selected_file))

    def _clear_selected_image(self):
        clear_image_button_clicked.emit()
