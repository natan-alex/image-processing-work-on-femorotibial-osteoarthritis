from app import App
from handlers.image_menu_events_handler import ImageMenuEventsHandler
from handlers.selection_menu_events_handler import SelectionMenuEventsHandler


class AppEventsHandlers:
    def __init__(self, app: App):
        self._image_menu_events_handler = ImageMenuEventsHandler(app)
        self._selection_menu_events_handler = SelectionMenuEventsHandler(app)
