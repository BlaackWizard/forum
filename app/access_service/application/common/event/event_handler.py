import logging
from typing import Generic
from abc import ABC

from app.access_service.application.common.event.event import EventT

class EventHandler(Generic[EventT], ABC):
    async def __call__(self, event: EventT) -> None:
        logging.info(f"Handling event: {event}")
