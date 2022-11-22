from typing import Callable, Union, Generic, List, TypeVar


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
