from app.access_service.domain.common.value_objects.base import ValueObject
from app.access_service.domain.exceptions.user import WeakPasswordError
from dataclasses import dataclass


@dataclass(frozen=True)
class UserName(ValueObject[str]):
    value: str

    def _validate(self):
        error_messages = {
            'Имя пользователя слишком длинное! (Максимум до 20 символов)': lambda x: len(x) <= 20,
            'Имя пользователя слишком короткое! (Минимум от 8 символов)': lambda x: len(x) > 8,
        }
        for msg, validator in error_messages:
            if not validator(self.value):
                raise WeakPasswordError(msg)
