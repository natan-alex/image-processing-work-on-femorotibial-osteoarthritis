import tkinter.filedialog as tk_files
from typing import Tuple
from PIL import Image as PilImages
from PIL.Image import Image

from configs import ALLOWED_IMAGE_FILE_TYPES


class ImageService:
    file_types = [
        ("Imagens", " ".join(ALLOWED_IMAGE_FILE_TYPES)),
        ("Todos os arquivos", "*.*")
    ]

    @staticmethod
    def open_image() -> Image:
        try:
            path = tk_files.askopenfilename(
                initialdir="~",
                title="Escolha uma imagem",
                filetypes=ImageService.file_types
            )

            return PilImages.open(path)
        except Exception as e:
            print(f"Exception on ImageService.open_image: {e}")
            return None

    @staticmethod
    def resize_image(image: Image, width: int, height: int) -> Image:
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
    def save_image(image: Image) -> bool:
        try:
            file_name = tk_files.asksaveasfile(
                initialdir="~",
                initialfile="Sem nome",
                defaultextension=ALLOWED_IMAGE_FILE_TYPES[0],
                filetypes=ImageService.file_types
            )

            image.save(file_name)
            return True
        except Exception as e:
            print(f"Exception on ImageService.save_image: {e}")
            return False

    @staticmethod
    def crop_image(
        image: Image,
        start_point: Tuple[int, int],
        end_point: Tuple[int, int],
        margin_left: int = 0,
        margin_top: int = 0,
    ) -> Image:
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
    def show_image(image: Image):
        try:
            image.show()
        except Exception as e:
            print(f"Exception on ImageService.show_image: {e}")
