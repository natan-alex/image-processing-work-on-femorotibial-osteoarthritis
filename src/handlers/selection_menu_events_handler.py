import tkinter.messagebox as tk_boxes
import tkinter.filedialog as tk_files

from app import App

from events.events import (
    select_image_button_clicked,
    clear_image_button_clicked,
    enter_selection_mode_button_clicked,
    clear_selection_button_clicked,
    leave_selection_mode_button_clicked,
    save_cropped_image_button_clicked,
    show_cropped_image_button_clicked,
    cross_correlation_calculated,
)


class SelectionMenuEventsHandler:
    """
    Class that can draw rectangles in the main screen
    and crop the selected image in the corresponding
    area
    """

    def __init__(self, app_instance: App):
        self._app = app_instance
        self._in_selection_mode = False
        self._rectangle = None
        self._start_x = 0
        self._start_y = 0
        self._end_x = 0
        self._end_y = 0

        self._listen_to_mouse_events()
        self._listen_to_app_events()

    def _listen_to_mouse_events(self):
        """
        Bind mouse events to the corresponding listeners
        """

        self._app.canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self._app.canvas.bind("<B1-Motion>", self._on_mouse_move)
        self._app.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

    def _listen_to_app_events(self):
        select_image_button_clicked.subscribe(
            self._on_select_image_button_clicked)
        clear_image_button_clicked.subscribe(
            self._on_clear_image_button_clicked)
        clear_selection_button_clicked.subscribe(
            self._on_clear_selection_button_clicked)
        enter_selection_mode_button_clicked.subscribe(
            self._on_enter_selection_mode_button_clicked)
        leave_selection_mode_button_clicked.subscribe(
            self._on_leave_selection_mode_button_clicked)
        save_cropped_image_button_clicked.subscribe(
            self._on_save_selection_image_button_clicked)
        show_cropped_image_button_clicked.subscribe(
            self._on_show_selection_image_button_clicked)
        cross_correlation_calculated.subscribe(
            self._cross_correlation_was_calculated)

    def _delete_rectangle(self):
        """
        Delete the rectangle selection if it exists
        """

        if self._rectangle is not None:
            self._app.canvas.delete(self._rectangle)
            self._rectangle = None

    def _create_rectangle_if_does_not_exist(self):
        """
        Create a small rectangle on the canvas if
        there is no rectangle yet
        """

        if self._rectangle is None:
            self._rectangle = self._app.canvas.create_rectangle(
                self._start_x, self._start_y,
                self._start_x + 1, self._start_y + 1,
                outline="red")

    def _move_rectangle_coordinates(self):
        """
        Moves the rectangle based on start_x, start_y,
        end_x and end_y values
        """

        if self._rectangle is not None:
            self._app.canvas.coords(
                self._rectangle,
                self._start_x, self._start_y,
                self._end_x, self._end_y)

    def _on_mouse_press(self, event):
        """
        Catch the event and set start_x and start_y
        variables with where the click happened
        It deletes the previous rectangle to avoid
        conflicts
        """

        if not self._in_selection_mode:
            return

        self._delete_rectangle()

        self._start_x = self._app.canvas.canvasx(event.x)
        self._start_y = self._app.canvas.canvasx(event.y)

    def _on_mouse_move(self, event):
        """
        Catch the mouse move event and set end_x and end_y
        variables with where the mouse is going
        """

        if not self._in_selection_mode:
            return

        self._create_rectangle_if_does_not_exist()

        self._end_x = self._app.canvas.canvasx(event.x)
        self._end_y = self._app.canvas.canvasy(event.y)

        self._move_rectangle_coordinates()

    def _on_mouse_release(self, event):
        """
        Catch the event and set end_x and end_y
        variables with where the mouse stopped
        """

        if (
            not self._in_selection_mode or
            self._rectangle is None or
            self._app.selected_image is None
        ):
            return

        margin_left, margin_top = self._app.canvas \
            .get_margins_for(self._app.selected_image)

        coordinates = (
            self._start_x - margin_left,
            self._start_y - margin_top,
            self._end_x - margin_left,
            self._end_y - margin_top,
        )

        self._app.cropped_image = self._app.selected_image.crop(coordinates)

    def _on_select_image_button_clicked(self):
        self._delete_rectangle()
        self._app.cropped_image = None

    def _on_clear_selection_button_clicked(self):
        self._delete_rectangle()
        self._app.cropped_image = None

    def _on_clear_image_button_clicked(self):
        self._delete_rectangle()
        self._app.cropped_image = None

    def _on_enter_selection_mode_button_clicked(self):
        """
        Allow user to draw something with the mouse
        """

        if self._in_selection_mode:
            return

        self._in_selection_mode = True
        self._app.canvas.configure(cursor="cross")

    def _on_leave_selection_mode_button_clicked(self):
        """
        Do not allow user to draw something with the mouse
        """

        if not self._in_selection_mode:
            return

        self._in_selection_mode = False
        self._delete_rectangle()
        self._app.canvas.configure(cursor="")
        self._app.cropped_image = None

    def _cross_correlation_was_calculated(self):
        """
        """

        correlation_points = self._app.cross_correlation_points

        if correlation_points is None:
            return

        self._delete_rectangle()

        start_point, end_point = correlation_points

        self._rectangle = self._app.canvas.create_rectangle(
            start_point[0], start_point[1],
            end_point[0], end_point[1],
            outline="blue"
        )

    def _on_show_selection_image_button_clicked(self):
        if self._app.cropped_image is not None:
            self._app.cropped_image.show()

    def _on_save_selection_image_button_clicked(self):
        if self._app.cropped_image is None:
            return

        try:
            file_name = tk_files.asksaveasfile(
                initialdir="~",
                initialfile="Sem nome",
                defaultextension=".jpg",
            )

            self._app.cropped_image.save(file_name)
            tk_boxes.showinfo(message="Imagem salva")
        except Exception:
            tk_boxes.showerror(message="Falha ao salvar imagem")
