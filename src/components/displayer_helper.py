from typing import Tuple

import tkinter.filedialog as tk_files
import tkinter.messagebox as tk_boxes
from PIL import Image


class DisplayerHelper:
    filetypes = [
        ("Imagens", "*.jpg .jpeg *.png"),
        ("Todos os arquivos", "*.*")
    ]

    @staticmethod
    def try_save_image(image: Image):
        if image is None:
            return

        try:
            file_name = tk_files.asksaveasfile(
                initialdir="~",
                initialfile="Sem nome",
                defaultextension=".jpg",
                filetypes=DisplayerHelper.filetypes
            )

            image.save(file_name)
            tk_boxes.showinfo(message="Imagem salva")
        except Exception:
            tk_boxes.showerror(message="Falha ao salvar imagem")

    @staticmethod
    def ask_open_image_and_get_result() -> Image:
        try:
            path = tk_files.askopenfilename(
                initialdir="~",
                title="Escolha uma imagem",
                filetypes=DisplayerHelper.filetypes,
            )

            return Image.open(path)
        except Exception:
            tk_boxes.showerror(message="Falha ao abrir imagem")

    @staticmethod
    def resize_image_if_necessary(
        image: Image,
        resize_to: Tuple[int, int]
    ) -> Image:
        if image is None:
            return None

        try:
            if image.size[0] > resize_to[0] and image.size[1] > resize_to[1]:
                return image.resize(resize_to, Image.ANTIALIAS)
        except Exception:
            return None
