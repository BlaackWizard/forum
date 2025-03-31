from datetime import datetime
from uuid import uuid4

from app.access_service.application.common.gateway import UserSaver
from app.access_service.application.common.token_sender import TokenSender
from app.access_service.application.common.interactor import Interactor
from dataclasses import dataclass

from app.access_service.application.common.uow import UoW
from app.access_service.application.dto import UserConfirmationTokenDTO, UserDTO
from app.access_service.domain.common.entities.timed_token import TimedTokenMetadata
from app.access_service.domain.common.value_objects.timed_token_id import TimedTokenId
from app.access_service.domain.entities.config import UserConfirmationTokenConfig
from app.access_service.domain.entities.confirmation_token import UserConfirmationToken
from app.access_service.domain.entities.user import UserEntity
from app.access_service.domain.services.password_hasher import PasswordHasher
from app.access_service.domain.value_objects.expires_in import ExpiresIn
from app.access_service.domain.value_objects.user_email import UserEmail
from app.access_service.domain.value_objects.user_id import UserId
from app.access_service.domain.value_objects.user_name import UserName
from app.access_service.domain.value_objects.user_raw_password import UserRawPassword


@dataclass
class RegisterUserDTO:
    email: str
    username: str
    password: str

class RegisterUser(Interactor[RegisterUserDTO, UserConfirmationTokenDTO]):
    def __init__(
        self,
        ph: PasswordHasher,
        uow: UoW,
        config: UserConfirmationTokenConfig,
        gateway: UserSaver,
        token_sender: TokenSender,
    ):
        self.ph = ph
        self.uow = uow
        self.config = config
        self.gateway = gateway
        self.token_sender = token_sender

    async def __call__(self, data: RegisterUserDTO) -> UserDTO:
        username = UserName(data.username)
        email = UserEmail(data.email)
        user_id = UserId(uuid4())

        user = UserEntity.create_with_raw_password(
            user_id=user_id,
            username=username,
            email=email,
            password_hasher=self.ph,
            raw_password=UserRawPassword(data.password)
        )
        user_dto = await self.gateway.save_user(user)
        await self.uow.commit()

        now = datetime.now()
        expires_in = ExpiresIn(now + self.config.expires_after)
        metadata = TimedTokenMetadata(expires_in=expires_in, uid=user_id)

        token_id = TimedTokenId(uuid4())
        token = UserConfirmationToken(
            metadata=metadata,
            token_id=token_id
        )

        token_dto = UserConfirmationTokenDTO(
            uid=token.uid.to_raw(),
            expires_in=token.expires_in.to_raw(),
            token_id=token.token_id.to_raw()
        )

        await self.token_sender.send(token_dto, user)

        return user_dto