from dataclasses import dataclass

from app.access_service.domain.common.entities.timed_token import TimedTokenUser
from app.access_service.domain.exceptions.token import AccessTokenIsExpiredError


@dataclass(frozen=True)
class AccessToken(TimedTokenUser):
    revoked: bool = False

    def verify(self) -> None:
        if self.expires_in.is_expired or self.revoked:
            raise AccessTokenIsExpiredError