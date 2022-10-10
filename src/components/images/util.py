import tkinter as tk
import tkinter.filedialog as tk_files
import tkinter.messagebox as tk_boxes
from typing import Union
from PIL import Image


class ImageUtil:
    default_file_name_separator = "__novo__"
    filetypes = [
        ("Imagens", "*.jpg *.png"),
        ("Todos os arquivos", "*.*")
    ]

    @staticmethod
    def save(image: Image):
        try:
            file_name = tk.filedialog.asksaveasfile(
                initialdir="~",
                initialfile="Sem nome",
                defaultextension="jpg",
                filetypes=ImageUtil.filetypes
            )

            image.save(file_name)
            tk_boxes.showinfo(message="Imagem salva")
        except Exception:
            tk_boxes.showerror(message="Falha ao salvar imagem")


class ImageOpenBuilder:
    def __init__(self):
        self._file_path: Union[str, None] = None
        self._image: Union[Image, None] = None

    def select(self):
        self._file_path = tk_files.askopenfilename(
            initialdir="~",
            title="Escolha uma imagem",
            filetypes=ImageUtil.filetypes,
        )

        return self

    def then_open(self):
        if self._file_path is None:
            return self

        try:
            self._image = Image.open(self._file_path)
            return self
        except Exception:
            tk_boxes.showerror(message="Falha ao abrir imagem")
            return self

    def then_resize_to(self, new_width: int, new_height: int):
        if self._image is None:
            return self

        try:
            resize_to = (new_width, new_height)
            self._image.thumbnail(resize_to, Image.ANTIALIAS)
            return self
        except Exception:
            return self

    def then_get_result(self):
        return self._image
