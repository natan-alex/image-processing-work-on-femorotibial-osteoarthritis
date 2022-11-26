from dataclasses import dataclass
from typing import Tuple
from events.event import Event


"""
All the events of the app with the corresponding
infos that they pass along the way when emitting an event
"""


select_image_button_clicked = Event()
clear_image_button_clicked = Event()
enter_selection_mode_button_clicked = Event()
clear_selection_button_clicked = Event()
leave_selection_mode_button_clicked = Event()
show_cropped_image_button_clicked = Event()
save_cropped_image_button_clicked = Event()
find_cross_correlation_button_clicked = Event()
equalize_histogram_button_clicked = Event()
cross_correlation_calculated = Event()
train_model_button_clicked = Event()


@dataclass
class RectangleFinishedDrawingEventInfos:
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]


rectangle_finished_drawing = Event[RectangleFinishedDrawingEventInfos]()
