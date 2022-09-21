from events.event import Event


class EventInfos:
    def __init__(self, selected_file: str):
        self.selected_file = selected_file


event = Event[EventInfos]()
