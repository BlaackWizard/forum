from app.access_service.domain.common.value_objects.base import ValueObject
from dataclasses import dataclass

@dataclass(frozen=True)
class UserHashedPassword(ValueObject[str]):
    value: str
