from dataclasses import dataclass

from app.access_service.domain.common.entities.timed_token import TimedTokenUser
from app.access_service.domain.exceptions.token import ConfirmationTokenIsExpiredError


class UserConfirmationToken(TimedTokenUser):
    def verify(self) -> None:
        if self.expires_in.is_expired:
            raise ConfirmationTokenIsExpiredError
