from dataclasses import dataclass
from uuid import UUID

from app.access_service.domain.common.value_objects.base import ValueObject

@dataclass(frozen=True)
class TimedTokenId(ValueObject[UUID]):
    value: UUID
