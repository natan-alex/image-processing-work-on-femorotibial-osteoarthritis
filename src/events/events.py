from PIL import Image
from events.event import Event, EventWithoutInfos


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
