from datetime import datetime
from uuid import uuid4

from app.access_service.application.common.exceptions.user import UserIsNotFoundError
from app.access_service.application.common.gateway import UserReader
from app.access_service.application.common.interactor import Interactor
from dataclasses import dataclass

from app.access_service.application.dto import AccessTokenDTO
from app.access_service.domain.common.entities.timed_token import TimedTokenMetadata
from app.access_service.domain.common.value_objects.timed_token_id import TimedTokenId
from app.access_service.domain.entities.access_token import AccessToken
from app.access_service.domain.entities.config import AccessTokenConfig
from app.access_service.domain.services.password_hasher import PasswordHasher
from app.access_service.domain.value_objects.expires_in import ExpiresIn
from app.access_service.domain.value_objects.user_email import UserEmail
from app.access_service.domain.value_objects.user_raw_password import UserRawPassword


@dataclass
class AuthorizeInputDTO:
    email: str
    password: str

class AuthorizeUser(Interactor[AuthorizeInputDTO, AccessTokenDTO]):
    def __init__(
        self,
        ph: PasswordHasher,
        config: AccessTokenConfig,
        gateway: UserReader,
    ):
        self.ph = ph
        self.config = config
        self.gateway = gateway

    async def __call__(self, data: AuthorizeInputDTO) -> AccessTokenDTO:
        user = await self.gateway.with_email(UserEmail(data.email))

        if not user:
            raise UserIsNotFoundError

        user.authenticate(raw_password=UserRawPassword(data.password), password_hasher=self.ph)
        user.ensure_is_active()

        now = datetime.now()
        expires_in = ExpiresIn(now + self.config.expires_after)
        metadata = TimedTokenMetadata(uid=user.user_id, expires_in=expires_in)

        token_id = TimedTokenId(uuid4())
        token = AccessToken(metadata, token_id)

        return AccessTokenDTO(
            uid=token.uid.to_raw(),
            expires_in=token.expires_in.to_raw(),
            token_id=token.token_id.to_raw(),
        )
