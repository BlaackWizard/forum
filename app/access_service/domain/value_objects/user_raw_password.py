from app.access_service.domain.common.value_objects.base import ValueObject
from dataclasses import dataclass
import re

from app.access_service.domain.exceptions.user import WeakPasswordError


def has_special_symbols(string: str) -> bool:
    regex = re.compile("[@_!#$%^&*()<>?/}{~:]")

    if re.search(regex, string) is None:
        return False

    return True

@dataclass(frozen=True)
class UserRawPassword(ValueObject[str]):
    value: str

    def _validate(self):
        error_messages = {
            'Пароль слишком короткий! (должен содержать как минимум 8 символов)': lambda x: len(x) > 8,
            'Пароль не содержит специальных символов! (@ % & *)': has_special_symbols,
            'Пароль не содержит заглавной буквы!': lambda x: any(s.issuper for s in x),
            'Пароль не должен состоять только из заглавных букв!': lambda x: any(s.islower for s in x)
        }
        for msg, validator in error_messages.items():
            if not validator(self.value):
                raise WeakPasswordError(msg)
