from typing import Callable, Generic, List, TypeVar


T = TypeVar("T")

EventHandler = Callable[[T], None]


class Event(Generic[T]):
    def __init__(self) -> None:
        super().__init__()
        self._event_handlers: List[EventHandler] = []

    def subscribe(self, handler: EventHandler):
        self._event_handlers.append(handler)

    def emit(self, infos: T):
        for callback in self._event_handlers:
            callback(infos)
