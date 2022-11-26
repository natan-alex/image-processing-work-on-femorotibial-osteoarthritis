import tkinter.messagebox as tk_boxes
from typing import Union

import aliases
from events import events
from components.window.main_window import MainWindow
from components.canvas.rectangle_drawer import RectangleDrawer

from services.image_service import ImageService
from services.correlation_service import CorrelationService
from services.training_model_service import TrainingModelService


class App:
    _selected_image: Union[aliases.Image, None] = None
    _cropped_image: Union[aliases.Image, None] = None
    _classes_and_files: Union[aliases.ClassesAndFiles, None] = None

    def __init__(self):
        self._main_window = MainWindow()
        self._main_canvas = self._main_window.main_canvas
        self._aside_box = self._main_window.aside_box
        self._rectangle_drawer = RectangleDrawer(self._main_canvas)

        self._handle_events()

    def run(self):
        self._main_canvas.display_no_image_message()
        self._main_window.mainloop()

    def _handle_events(self):
        events.select_image_button_clicked.subscribe(self._on_select_image_button_clicked)
        events.clear_image_button_clicked.subscribe(self._on_clear_image_button_clicked)
        events.enter_selection_mode_button_clicked.subscribe(self._on_enter_selection_mode_button_clicked)
        events.leave_selection_mode_button_clicked.subscribe(self._on_leave_selection_mode_button_clicked)
        events.clear_selection_button_clicked.subscribe(self._on_clear_selection_button_clicked)
        events.rectangle_finished_drawing.subscribe(self._on_rectangle_finished_drawing)
        events.show_cropped_image_button_clicked.subscribe(self._on_show_cropped_image_button_clicked)
        events.save_cropped_image_button_clicked.subscribe(self._on_save_cropped_image_button_clicked)
        events.find_cross_correlation_button_clicked.subscribe(self._on_find_cross_correlation_button_clicked)
        events.train_model_button_clicked.subscribe(self._on_train_model_button_clicked)

    def _on_select_image_button_clicked(self):
        self._selected_image = ImageService.open_image()

        if self._selected_image is None:
            tk_boxes.showerror(message="Falha ao abrir arquivo")
            return

        self._selected_image = ImageService.resize_image(
            self._selected_image,
            self._main_canvas.winfo_width(),
            self._main_canvas.winfo_height())

        self._rectangle_drawer.deactivate()
        self._main_canvas.display_image(self._selected_image)

    def _on_clear_image_button_clicked(self):
        self._rectangle_drawer.deactivate()
        self._main_canvas.display_no_image_message()
        self._selected_image = None
        self._cropped_image = None

    def _on_enter_selection_mode_button_clicked(self):
        if self._selected_image is None:
            tk_boxes.showwarning(message="Nenhuma imagem foi escolhida ainda")
            return

        self._rectangle_drawer.activate()

    def _on_leave_selection_mode_button_clicked(self):
        self._rectangle_drawer.deactivate()
        self._cropped_image = None

    def _on_clear_selection_button_clicked(self):
        self._cropped_image = None
        self._rectangle_drawer.delete_rectangle()

    def _on_rectangle_finished_drawing(
        self, event_infos: events.RectangleFinishedDrawingEventInfos
    ):
        margin_left, margin_top = self._main_canvas. \
            get_margins_for(self._selected_image)

        self._cropped_image = ImageService.crop_image(
            self._selected_image,
            event_infos.start_point, event_infos.end_point,
            margin_left, margin_top)

    def _on_show_cropped_image_button_clicked(self):
        if self._cropped_image is None:
            tk_boxes.showwarning(message="Nenhuma seleção foi feita ainda")
            return

        ImageService.show_image(self._cropped_image)

    def _on_save_cropped_image_button_clicked(self):
        if self._cropped_image is None:
            tk_boxes.showwarning(message="Nenhuma seleção foi feita ainda")
            return

        ImageService.save_image(self._cropped_image)

    def _on_find_cross_correlation_button_clicked(self):
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

        margin_left, margin_top = self._main_canvas. \
            get_margins_for(self._selected_image)

        self._rectangle_drawer.draw_rectangle(
            start_point=(start_point[0] + margin_left, start_point[1] + margin_top),
            end_point=(end_point[0] + margin_left, end_point[1] + margin_top))

    def _on_train_model_button_clicked(self):
        result = TrainingModelService.read_model_related_folders_and_files()

        if result.error is not None:
            tk_boxes.showerror("Falha ao treinar modelo", message=result.error)
            return

        self._folders_classes_and_files = result.folder_classes_and_files

        self._aside_box.display_folders_classes_and_files_infos(
            self._folders_classes_and_files)
