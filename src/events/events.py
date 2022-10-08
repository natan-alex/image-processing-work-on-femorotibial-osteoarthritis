from events.event import Event


class FileSelectedEventInfos:
    def __init__(self, selected_file: str):
        self.selected_file = selected_file


file_selected_event = Event[FileSelectedEventInfos]()
clear_image_button_clicked = Event()
