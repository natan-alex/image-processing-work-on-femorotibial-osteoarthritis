import tkinter.messagebox as tk_boxes
import tkinter.filedialog as tk_files
from PIL import Image, ImageTk

from app import App
from services.correlation_service import CorrelationService
from events.events import (
    select_image_button_clicked,
    clear_image_button_clicked,
    find_cross_correlation_button_clicked,
    cross_correlation_calculated,
)


class ImageMenuEventsHandler:
    """
    Class responsible for displaying the selected
    image and listen to all menu events, also cordinating
    the drawer actions
    """

    _file_types = [
        ("Imagens", "*.jpg .jpeg *.png"),
        ("Todos os arquivos", "*.*")
    ]

    def __init__(self, app_instance: App):
        self._app = app_instance
        self._photo_image = None
        self._text_container = None
        self._image_container = None

        self._subscribe_to_events()
        self._create_text_container_with_no_image_message()

    def _subscribe_to_events(self):
        select_image_button_clicked.subscribe(
            self._on_select_image_button_clicked)
        clear_image_button_clicked.subscribe(
            self._on_clear_image_button_clicked)
        find_cross_correlation_button_clicked.subscribe(
            self._on_find_cross_correlation_button_clicked)

    def _create_text_container_with_no_image_message(self):
        """
        Create a text inside the main screen
        saying that no image was selected
        """

        self._text_container = self._app.canvas.create_text(
            self._app.canvas.winfo_width() / 2,
            self._app.canvas.winfo_height() / 2,
            text="Nenhuma imagem selecionada")

    def _create_image_container(self):
        """
        Create a space inside the main screen
        to display the selected image
        """

        if self._photo_image is None:
            return

        if self._image_container is not None:
            self._app.canvas.delete(self._image_container)

        self._image_container = self._app.canvas.create_image(
            self._app.canvas.winfo_width() / 2,
            self._app.canvas.winfo_height() / 2,
            image=self._photo_image)

    def _open_image(self) -> Image.Image:
        try:
            path = tk_files.askopenfilename(
                initialdir="~",
                title="Escolha uma imagem",
                filetypes=ImageMenuEventsHandler._file_types,
            )

            return Image.open(path)
        except Exception:
            tk_boxes.showerror(message="Falha ao abrir imagem")

    def _resize_image_to_fit_on_canvas(self, image: Image) -> Image.Image:
        try:
            width = self._app.canvas.winfo_width()
            height = self._app.canvas.winfo_height()

            if image.size[0] > width and image.size[1] > height:
                return image.resize((width, height), Image.ANTIALIAS)
            else:
                return image
        except Exception:
            return image

    def _on_select_image_button_clicked(self):
        """
        Handle for select image menu item click event
        Opens the file and show the image in the screen
        """

        image = self._open_image()

        if image is None:
            return

        image = self._resize_image_to_fit_on_canvas(image)
        self._photo_image = ImageTk.PhotoImage(image)
        self._app.selected_image = image

        if self._text_container is not None:
            self._app.canvas.delete(self._text_container)

        self._create_image_container()

    def _on_clear_image_button_clicked(self):
        """
        Handle for clear image menu item click event
        """

        if self._image_container is not None:
            self._app.canvas.delete(self._image_container)

        self._create_text_container_with_no_image_message()

    def _on_find_cross_correlation_button_clicked(self):
        if self._app.selected_image is None:
            return

        template_image = self._open_image()

        if template_image is None:
            return

        correlation_points = CorrelationService \
            .find_cross_correlation_between(
                self._app.selected_image,
                template_image)

        if correlation_points is None:
            return

        start_point, end_point = correlation_points

        margin_left, margin_top = self._app.canvas \
            .get_margins_for(self._app.selected_image)

        self._app.cross_correlation_points = (
            (start_point[0] + margin_left, start_point[1] + margin_top),
            (end_point[0] + margin_left, end_point[1] + margin_top)
        )

        cross_correlation_calculated.emit()
