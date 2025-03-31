from typing import TypeVar, Any
from abc import ABC

class Event(ABC):
    def __str__(self):
        return self.__class__.__name__

EventT = TypeVar("EventT", bound=Event)
EventsT = TypeVar("EventsT", bound=Event)

