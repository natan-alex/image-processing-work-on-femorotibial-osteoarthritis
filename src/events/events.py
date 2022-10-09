from events.event import Event, EventWithoutInfos


class FileSelectedEventInfos:
    def __init__(self, selected_file: str):
        self.selected_file = selected_file


file_selected_event = Event[FileSelectedEventInfos]()
clear_image_button_clicked = EventWithoutInfos()
clear_selection_button_clicked = EventWithoutInfos()
select_area_button_clicked = EventWithoutInfos()
