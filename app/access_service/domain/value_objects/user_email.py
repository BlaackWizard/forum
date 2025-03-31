from app.access_service.domain.common.value_objects.base import ValueObject
from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError

from app.access_service.domain.exceptions.user import UserEmailIsIncorrect


@dataclass(frozen=True)
class UserEmail(ValueObject[str]):
    value: str

    def _validate(self):
        try:
            validate_email(self.value, check_deliverability=False)
        except EmailNotValidError as exc:
            raise UserEmailIsIncorrect from exc
