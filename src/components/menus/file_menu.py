import tkinter as tk
import tkinter.filedialog as tk_files
from events.file_was_selected import event, EventInfos


class FileMenu(tk.Menu):
    def __init__(self, parent: tk.Menu):
        tk.Menu.__init__(self, master=parent, tearoff=False)
        self._setup()

    def _setup(self):
        self.add_command(
            label="Abrir",
            command=self._open_file_explorer
        )

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

        if not selected_file:
            return

        event.emit(EventInfos(selected_file))
