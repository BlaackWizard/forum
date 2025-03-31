from abc import ABC
from typing import Generic, Any, TypeVar
from dataclasses import dataclass


V = TypeVar('V', bound=Any)

@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self):
        self._validate()

    def _validate(self): ...

@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[V]):
    value: V

    def to_raw(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return self.value == other
        return self.value == other.value

