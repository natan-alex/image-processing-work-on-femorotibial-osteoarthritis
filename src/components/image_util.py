import tkinter as tk
import tkinter.filedialog as tk_files
import tkinter.messagebox as tk_boxes
import cv2
import numpy as np
from typing import Tuple
from PIL import Image


class ImageUtil:
    filetypes = [
        ("Imagens", "*.jpg *.png"),
        ("Todos os arquivos", "*.*")
    ]

    @staticmethod
    def get_left_and_top_margins_from_image_to_canvas(
        image: Image,
        canvas: tk.Canvas
    ) -> Tuple[int, int]:
        width_diff = canvas.winfo_width() - image.size[0]
        height_diff = canvas.winfo_height() - image.size[1]
        return (width_diff / 2, height_diff / 2)

    @staticmethod
    def transform_point_considering_image_distance_to_canvas(
        canvas: tk.Canvas,
        image: Image,
        point: Tuple[int, int]
    ) -> Tuple[int, int]:
        distances = ImageUtil.get_left_and_top_margins_from_image_to_canvas(image, canvas)
        return (
            point[0] + distances[0],
            point[1] + distances[1],
        )

    @staticmethod
    def ask_to_open_file() -> str:
        return tk_files.askopenfilename(
            initialdir="~",
            title="Escolha uma imagem",
            filetypes=ImageUtil.filetypes,
        )

    @staticmethod
    def try_open(path: str):
        try:
            return Image.open(path)
        except Exception:
            tk_boxes.showerror(message="Falha ao abrir imagem")

    @staticmethod
    def try_resize(image: Image, new_width: int, new_height: int):
        try:
            resize_to = (new_width, new_height)
            image.thumbnail(resize_to, Image.ANTIALIAS)
        except Exception:
            pass

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

    @staticmethod
    def find_cross_correlation_between(
        image: Image,
        template: Image,
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        image_as_np_array = np.array(image)
        template_as_np_array = np.array(template)
        correlation = cv2.matchTemplate(
            image_as_np_array,
            template_as_np_array,
            cv2.TM_CCOEFF_NORMED
        )
        template_height, template_width, _ = template_as_np_array.shape
        argmax = np.argmax(correlation)
        location_y, location_x = np.unravel_index(argmax, correlation.shape)
        return (
            (location_x, location_y),
            (location_x + template_width, location_y + template_height)
        )
