import tkinter as tk
from PIL import Image, ImageTk
from events.file_was_selected import (
    event as file_selected_event,
    EventInfos as FileSelectedEventInfos
)


class ImageDisplayer(tk.Frame):
    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self._label_image: ImageTk = None
        self._label = tk.Label(self)
        self._setup()

    def _setup(self):
        self.configure(width=400, height=600)
        self.pack()
        self.place(anchor='center', relx=0.5, rely=0.5)

        self._label.configure(text="Nenhuma imagem selecionada")
        self._label.pack()

        file_selected_event.subscribe(self._on_file_selected)

    def _on_file_selected(self, event_infos: FileSelectedEventInfos):
        image = Image.open(event_infos.selected_file)
        self._label_image = ImageTk.PhotoImage(image)
        self._label.configure(image=self._label_image)

    @property
    def label(self) -> tk.Label:
        return self._label
