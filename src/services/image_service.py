import cv2
import numpy as np
import tkinter.filedialog as tk_files
from PIL import Image as PilImages, ImageOps
from typing import Tuple, Union

from globals import aliases, configs


class ImageService:
    file_types = [
        ("Imagens", " ".join(configs.ALLOWED_IMAGE_FILE_TYPES)),
        ("Todos os arquivos", "*.*")
    ]

    @staticmethod
    def open_image() -> Union[aliases.Image, None]:
        try:
            path = tk_files.askopenfilename(
                initialdir="~",
                title="Escolha uma imagem",
                filetypes=ImageService.file_types
            )

            if path is None:
                return None

            return PilImages.open(path)
        except Exception as e:
            print(f"Exception on ImageService.open_image: {e}")
            return None

    @staticmethod
    def resize_image(
        image: aliases.Image,
        width: int,
        height: int
    ) -> Union[aliases.Image, None]:
        if image is None:
            return None

        try:
            image_width = image.size[0]
            image_height = image.size[1]
            new_image_width = image_width
            new_image_height = image_height

            if image_width > width and image_height > height:
                new_image_width = width
                new_image_height = height
            elif image_width > width:
                new_image_width = width
            elif image_height > height:
                new_image_height = height

            new_size = (new_image_width, new_image_height)
            return image.resize(new_size, PilImages.ANTIALIAS)
        except Exception as e:
            print(f"Exception on ImageService.resize_image: {e}")
            return image

    @staticmethod
    def save_image(image: aliases.Image) -> bool:
        if image is None:
            return False

        try:
            file_name = tk_files.asksaveasfile(
                initialdir="~",
                initialfile="Sem nome",
                defaultextension=configs.ALLOWED_IMAGE_FILE_TYPES[0],
                filetypes=ImageService.file_types
            )

            if file_name is None:
                return False

            image.save(file_name)
            return True
        except Exception as e:
            print(f"Exception on ImageService.save_image: {e}")
            return False

    @staticmethod
    def crop_image(
        image: aliases.Image,
        start_point: Tuple[int, int],
        end_point: Tuple[int, int],
        margin_left: int = 0,
        margin_top: int = 0,
    ) -> Union[aliases.Image, None]:
        if image is None:
            return image

        try:
            coordinates = (
                start_point[0] - margin_left, start_point[1] - margin_top,
                end_point[0] - margin_left, end_point[1] - margin_top,
            )

            return image.crop(coordinates)
        except Exception as e:
            print(f"Exception on ImageService.crop_image: {e}")
            return image

    @staticmethod
    def show_image(image: aliases.Image):
        if image is None:
            return

        try:
            image.show()
        except Exception as e:
            print(f"Exception on ImageService.show_image: {e}")

    @staticmethod
    def equalize_histogram(image: aliases.Image) -> Union[aliases.Image, None]:
        if image is None:
            return None

        try:
            image_array = np.array(image)
            equalized = cv2.equalizeHist(image_array)
            return PilImages.fromarray(equalized)
        except Exception as e:
            print(f"Exception on ImageService.equalize_histogram: {e}")
            return image

    @staticmethod
    def flip_horizontally(image: aliases.Image) -> Union[aliases.Image, None]:
        if image is None:
            return None

        try:
            return ImageOps.mirror(image)
        except Exception as e:
            print(f"Exception on ImageService.flip_horizontally: {e}")
            return None
