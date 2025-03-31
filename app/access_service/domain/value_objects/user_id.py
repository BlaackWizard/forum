from uuid import UUID
from dataclasses import dataclass

from app.access_service.domain.common.value_objects.base import ValueObject

@dataclass(frozen=True)
class UserId(ValueObject[UUID]):
    value: UUID
