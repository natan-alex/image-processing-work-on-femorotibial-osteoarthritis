from PIL import Image
from events.event import Event, EventWithoutInfos


"""
All the events of the app with the corresponding
infos that they pass along the way when emitting an event
"""


class AreaSelectionFinishedEventInfos:
    def __init__(self, cropped_image: Image):
        self.cropped_image = cropped_image


select_image_button_clicked = EventWithoutInfos()
clear_image_button_clicked = EventWithoutInfos()
clear_selection_button_clicked = EventWithoutInfos()
enter_selection_mode_button_clicked = EventWithoutInfos()
leave_selection_mode_button_clicked = EventWithoutInfos()
area_selection_finished = Event[AreaSelectionFinishedEventInfos]()
show_cropped_image_button_clicked = EventWithoutInfos()
save_cropped_image_button_clicked = EventWithoutInfos()
find_cross_correlation_button_clicked = EventWithoutInfos()
