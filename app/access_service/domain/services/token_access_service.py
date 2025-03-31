from dataclasses import dataclass

from app.access_service.domain.common.services.access_service import AccessService
from app.access_service.domain.entities.access_token import AccessToken
from app.access_service.domain.entities.user import UserEntity
from app.access_service.domain.exceptions.token import AccessTokenIsExpiredError
from app.access_service.domain.exceptions.user import UserIsNotActiveError, UnauthorizedError


@dataclass(frozen=True)
class TokenAccessService(AccessService):
    token: AccessToken

    def authorize(self, user: UserEntity) -> None:
        try:
            self.token.verify()
            user.ensure_is_active()

        except (AccessTokenIsExpiredError, UserIsNotActiveError) as exc:
            raise exc from UnauthorizedError

        if self.token.uid != user.user_id:
            raise UnauthorizedError
