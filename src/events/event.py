from typing import Callable, Generic, List, TypeVar


T = TypeVar("T")

EventHandler = Callable[[T], None]


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
        self._event_handlers: List[EventHandler] = []

    def subscribe(self, handler: EventHandler):
        self._event_handlers.append(handler)

    def emit(self, infos: T):
        for callback in self._event_handlers:
            callback(infos)


EventWithoutInfosHandler = Callable[[], None]


class EventWithoutInfos():
    """
    Very similar to event class, but cannot
    notify the observers with any information
    """

    def __init__(self) -> None:
        super().__init__()
        self._event_handlers: List[EventWithoutInfosHandler] = []

    def subscribe(self, handler: EventWithoutInfosHandler):
        self._event_handlers.append(handler)

    def emit(self):
        for callback in self._event_handlers:
            callback()
