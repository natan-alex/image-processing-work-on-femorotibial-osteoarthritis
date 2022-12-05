import tkinter as tk
from typing import Tuple
from PIL import ImageTk

from globals import aliases


class Canvas(tk.Canvas):
    """
    A canvas for displaying the selected image
    and drawing rectangles to crop the image
    """

    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self.configure(width=parent.winfo_width())
        self.configure(height=parent.winfo_height())

        self.pack(fill=tk.BOTH)

        self.update()

        self._text_container = None
        self._image_container = None

    def get_margins_for(self, image: aliases.Image) -> Tuple[int, int]:
        """
        Computes the space between the window and the image
        on center, the space from the (0, 0) to the top left
        corner of the image
        """

        canvas_width, canvas_height = (self.winfo_width(), self.winfo_height())
        image_width, image_height = (image.size[0], image.size[1])
        margin_left, margin_top = (0, 0)

        if canvas_width > image_width:
            margin_left = (canvas_width - image_width) / 2

        if canvas_height > image_height:
            margin_top = (canvas_height - image_height) / 2

        return (margin_left, margin_top)

    def _delete_existing_containers(self):
        if self._text_container is not None:
            self.delete(self._text_container)

        if self._image_container is not None:
            self.delete(self._image_container)

    def display_no_image_message(self):
        """
        Create a text inside the canvas
        saying that no image was selected
        """

        self._delete_existing_containers()

        self._text_container = self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text="Nenhuma imagem selecionada")

    def display_image(self, image: aliases.Image):
        """
        Create a space inside the canvas to display the image
        """

        self._delete_existing_containers()

        self._photo_image = ImageTk.PhotoImage(image)

        self._image_container = self.create_image(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            image=self._photo_image)
