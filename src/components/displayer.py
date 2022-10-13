import tkinter as tk
from PIL import ImageTk

from events.events import *
from configs import APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT
from components.image_util import ImageUtil
from components.drawer import Drawer


class Displayer(tk.Canvas):
    """
    Class responsible for displaying the selected
    image and listen to all menu events, also cordinating
    the drawer actions
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(
            parent,
            width=APP_DEFAULT_WIDTH,
            height=APP_DEFAULT_HEIGHT,
            borderwidth=0,
            highlightthickness=0)

        self._canvas_width = APP_DEFAULT_WIDTH
        self._canvas_height = APP_DEFAULT_HEIGHT
        self._drawer = Drawer(self)
        self._text_container = None
        self._image_container = None
        self._image = None
        self._photo_image = None
        self._cropped_image = None
        self._setup()

    def _create_text_container_with_no_image_message(self):
        """
        Create a text inside the main screen
        saying that no image was selected
        """

        self._text_container = self.create_text(
            self._canvas_width / 2,
            self._canvas_height / 2,
            text="Nenhuma imagem selecionada")

    def _create_image_container(self):
        """
        Create a space inside the main screen
        to display the selected image
        """

        if self._photo_image is None:
            return

        self._image_container = self.create_image(
            self._canvas_width / 2,
            self._canvas_height / 2,
            image=self._photo_image)

    def _setup(self):
        """
        Init component things, place itself in the app
        and listen to all menu events to handle them
        """

        self._create_text_container_with_no_image_message()
        self.pack(fill=tk.BOTH, anchor=tk.NW, padx=0, pady=0)

        select_image_button_clicked.subscribe(
            self._on_select_image_button_click)
        clear_image_button_clicked.subscribe(
            self._on_clear_image_button_click)
        clear_selection_button_clicked.subscribe(
            self._on_clear_selection_button_click)
        enter_selection_mode_button_clicked.subscribe(
            self._on_enter_selection_mode_button_click)
        leave_selection_mode_button_clicked.subscribe(
            self._on_leave_selection_mode_button_click)
        show_cropped_image_button_clicked.subscribe(
            self._on_show_cropped_image_button_click)
        area_selection_finished.subscribe(
            self._on_area_selection_finished)
        save_cropped_image_button_clicked.subscribe(
            self._on_save_cropped_image_button_click)
        find_cross_correlation_button_clicked.subscribe(
            self._on_find_cross_correlation_button_click)

    def _on_select_image_button_click(self):
        """
        Handle for select image menu item click event
        Opens the file and show the image in the screen
        """

        image_path = ImageUtil.ask_to_open_file()

        if image_path is None:
            return

        image = ImageUtil.try_open(image_path)

        if image is None:
            return

        if self._text_container is not None:
            self.delete(self._text_container)

        self._image = image
        self._photo_image = ImageTk.PhotoImage(image)
        self._create_image_container()

    def _on_clear_image_button_click(self):
        """
        Handle for clear image menu item click event
        Clear image being displayed,
        deactivate drawer and display
        message with no image
        """

        if self._image_container is not None:
            self.delete(self._image_container)

        self._image = None
        self._photo_image = None
        self._cropped_image = None
        self._drawer.deactivate()
        self._create_text_container_with_no_image_message()

    def _on_clear_selection_button_click(self):
        """
        Handle for clear selected area menu item click event
        Just clear the selection and the variable
        that holds the corresponding cropped image
        """

        self._drawer.clear_selection()
        self._cropped_image = None

    def _on_enter_selection_mode_button_click(self):
        """
        Handle for enter selection mode menu item click event
        Activate drawer and set its image
        """

        if self._image is not None:
            self._drawer.activate()
            self._drawer.set_selected_image(self._image)

    def _on_leave_selection_mode_button_click(self):
        """
        Handler for leave selection mode menu item click event
        Deactivate the drawer and clear the cropped image
        """

        self._drawer.deactivate()
        self._cropped_image = None

    def _on_area_selection_finished(
        self,
        event: AreaSelectionFinishedEventInfos
    ):
        """
        Handler for when the area was been drawn
        Just store the cropped image for further use
        """

        if not self._drawer.is_activated:
            return

        if not self._drawer.has_selection:
            return

        if self._image is None:
            return

        self._cropped_image = event.cropped_image

    def _on_show_cropped_image_button_click(self):
        """
        Handler for show cropped image menu item click event
        Shows the cropped image in an external app
        """

        if self._cropped_image is None:
            return

        self._cropped_image.show()

    def _on_save_cropped_image_button_click(self):
        """
        Handler for save cropped image menu item click event
        Just try to save the cropped image
        """

        if self._cropped_image is None:
            return

        ImageUtil.save(self._cropped_image)

    def _on_find_cross_correlation_button_click(self):
        """
        Handler for find cross correlation menu item click event
        Ask for the image to correlate with and display the
        correlation found with a rectangle in the screen
        """

        if self._image is None:
            return

        template_path = ImageUtil.ask_to_open_file()

        if template_path is None:
            return

        template_image = ImageUtil.try_open(template_path)

        if template_image is None:
            return

        start_point, end_point = ImageUtil.find_cross_correlation_between(
            self._image,
            template_image)

        self._drawer.draw_rectangle_considering_image_margins(
            start_point, end_point)
