from dataclasses import dataclass
from datetime import datetime

from app.access_service.domain.common.value_objects.base import ValueObject

@dataclass(frozen=True)
class ExpiresIn(ValueObject[datetime]):
    value: datetime

    @property
    def is_expired(self):
        if self.value < datetime.now():
            return False
        return True
