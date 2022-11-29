from dataclasses import dataclass
from typing import Callable, Union, Generic, List, TypeVar, Tuple


"""
All the events of the app with the corresponding
infos that they pass along the way when emitting an event
"""


T = TypeVar("T")

EventWithInfosHandler = Callable[[T], None]
EventWithoutInfosHandler = Callable[[], None]
Handler = Union[EventWithInfosHandler, EventWithoutInfosHandler]


class Event(Generic[T]):
    """
    Class that represents an event, with possibilities
    to notify the subscribers when the event occurr and
    subscribe to it
    This event carries some information to pass to its
    subscribers
    """

    def __init__(self) -> None:
        super().__init__()
        self._event_handlers: List[Handler] = []

    def subscribe(self, handler: Handler):
        self._event_handlers.append(handler)

    def emit(self, infos: Union[T, None] = None):
        for callback in self._event_handlers:
            if infos is None:
                callback()
            else:
                callback(infos)


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
read_model_main_directory_button_clicked = Event()
histogram_equalization_button_clicked = Event()
horizontal_mirroring_button_clicked = Event()
train_neural_network_button_clicked = Event()
train_normal_classifier_button_clicked = Event()


@dataclass
class RectangleFinishedDrawingEventInfos:
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]


rectangle_finished_drawing = Event[RectangleFinishedDrawingEventInfos]()
