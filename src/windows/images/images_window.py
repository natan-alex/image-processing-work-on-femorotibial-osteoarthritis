import tkinter as tk
import tkinter.messagebox as tk_boxes
from typing import Union

from globals import configs, aliases, events

from windows.images.menus.menu_bar import MenuBar
from windows.images.components.canvas import Canvas

from helpers.rectangle_drawer import RectangleDrawer

from services.image_service import ImageService
from services.correlation_service import CorrelationService


class ImagesWindow(tk.Toplevel):
    """
    Class that represents the images window.
    Contains menus to realize operations on images,
    as open an image, display it, crop it using
    a drawn rectangle, etc
    """

    _selected_image: Union[aliases.Image, None] = None
    _cropped_image: Union[aliases.Image, None] = None
    _equalized_image: Union[aliases.Image, None] = None
    _flipped_image: Union[aliases.Image, None] = None

    def __init__(self):
        super().__init__()

        self.title("Imagens")
        self.configure(width=configs.IMAGES_WINDOW_WIDTH)
        self.configure(height=configs.IMAGES_WINDOW_HEIGHT)
        self.resizable(False, False)
        self.update()

        self._init_components()
        self._handle_events()

    def _init_components(self):
        """ Init necessary components """

        self.config(menu=MenuBar(self))

        self._canvas = Canvas(self)
        self._rectangle_drawer = RectangleDrawer(self._canvas)

        self._canvas.display_no_image_message()

    def _handle_events(self):
        """ Just subscribe to the image related events """

        events.select_image_button_clicked.subscribe(self._on_select_image_button_clicked)
        events.clear_image_button_clicked.subscribe(self._on_clear_image_button_clicked)
        events.enter_selection_mode_button_clicked.subscribe(self._on_enter_selection_mode_button_clicked)
        events.leave_selection_mode_button_clicked.subscribe(self._on_leave_selection_mode_button_clicked)
        events.clear_selection_button_clicked.subscribe(self._on_clear_selection_button_clicked)
        events.rectangle_finished_drawing.subscribe(self._on_rectangle_finished_drawing)
        events.show_cropped_image_button_clicked.subscribe(self._on_show_cropped_image_button_clicked)
        events.save_cropped_image_button_clicked.subscribe(self._on_save_cropped_image_button_clicked)
        events.find_cross_correlation_button_clicked.subscribe(self._on_find_cross_correlation_button_clicked)
        events.histogram_equalization_button_clicked.subscribe(self._on_histogram_equalization_button_clicked)
        events.horizontal_mirroring_button_clicked.subscribe(self._on_horizontal_mirroring_button_clicked)

    def _on_select_image_button_clicked(self):
        """
        Open the file explorer for the user to
        select an image and display the selected one
        """

        self._selected_image = ImageService.open_image()

        if self._selected_image is None:
            tk_boxes.showerror(message="Falha ao abrir arquivo")
            return

        self._selected_image = ImageService.resize_image(
            self._selected_image,
            self._canvas.winfo_width(),
            self._canvas.winfo_height())

        self._rectangle_drawer.deactivate()
        self._canvas.display_image(self._selected_image)

    def _on_clear_image_button_clicked(self):
        """ Just removes the image being displayed """

        self._rectangle_drawer.deactivate()
        self._canvas.display_no_image_message()
        self._selected_image = None
        self._cropped_image = None

    def _on_enter_selection_mode_button_clicked(self):
        """ Make possible for the user to draw rectangles to make selections """

        if self._selected_image is None:
            tk_boxes.showwarning(message="Nenhuma imagem foi escolhida ainda")
            return

        self._rectangle_drawer.activate()

    def _on_leave_selection_mode_button_clicked(self):
        """ Disable the rectangle drawer and remove previous selection """

        self._rectangle_drawer.deactivate()
        self._cropped_image = None

    def _on_clear_selection_button_clicked(self):
        """ Remove previous selection """

        self._cropped_image = None
        self._rectangle_drawer.delete_rectangle()

    def _on_rectangle_finished_drawing(
        self, event_infos: events.RectangleFinishedDrawingEventInfos
    ):
        """
        After the rectangle being drawn, crop the selected image 
        in the area considering its margins to the canvas
        """

        margin_left, margin_top = self._canvas. \
            get_margins_for(self._selected_image)

        self._cropped_image = ImageService.crop_image(
            self._selected_image,
            event_infos.start_point, event_infos.end_point,
            margin_left, margin_top)

    def _on_show_cropped_image_button_clicked(self):
        """ Show the selection as an image """

        if self._cropped_image is None:
            tk_boxes.showwarning(message="Nenhuma seleção foi feita ainda")
            return

        ImageService.show_image(self._cropped_image)

    def _on_save_cropped_image_button_clicked(self):
        """ Save selection into file system """

        if self._cropped_image is None:
            tk_boxes.showwarning(message="Nenhuma seleção foi feita ainda")
            return

        ImageService.save_image(self._cropped_image)

    def _on_find_cross_correlation_button_clicked(self):
        """
        Ask the user the other image to correlate with. After 
        finding the correlation, draw it as a rectangle on the screen
        """

        if self._selected_image is None:
            tk_boxes.showwarning(message="Necessário selecionar uma imagem antes")
            return

        template_image = ImageService.open_image()

        if template_image is None:
            tk_boxes.showerror(message="Nenhuma imagem escolhida para encontrar a correlação")
            return

        correlation_points = CorrelationService \
            .find_cross_correlation_between(self._selected_image, template_image)

        if correlation_points is None:
            tk_boxes.showerror(message="Falha ao encontrar correlação entre imagens")
            return

        start_point, end_point = correlation_points

        margin_left, margin_top = self._canvas. \
            get_margins_for(self._selected_image)

        self._rectangle_drawer.draw_rectangle(
            start_point=(start_point[0] + margin_left, start_point[1] + margin_top),
            end_point=(end_point[0] + margin_left, end_point[1] + margin_top))

    def _on_histogram_equalization_button_clicked(self):
        """
        Equalize the selected image histogram and display 
        the resulting image
        """
        if self._selected_image is None:
            tk_boxes.showwarning(message="Necessário selecionar uma imagem antes")
            return

        self._equalized_image = ImageService.equalize_histogram(self._selected_image)

        if self._equalized_image is None:
            tk_boxes.showerror("Falha ao equalizar histograma da imagem")
            return

        ImageService.show_image(self._equalized_image)

        if tk_boxes.askquestion("Salvar", "Deseja salvar a imagem?") == "yes":
            ImageService.save_image(self._equalized_image)

    def _on_horizontal_mirroring_button_clicked(self):
        """ Flip image horizontally and display it """

        if self._selected_image is None:
            tk_boxes.showwarning(message="Necessário selecionar uma imagem antes")
            return

        self._flipped_image = ImageService.flip_horizontally(self._selected_image)

        if self._flipped_image is None:
            tk_boxes.showerror("Falha ao realizar espelhamento horizontal da imagem")
            return

        ImageService.show_image(self._flipped_image)

        if tk_boxes.askquestion("Salvar", "Deseja salvar a imagem?") == "yes":
            ImageService.save_image(self._flipped_image)
