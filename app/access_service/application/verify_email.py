from app.access_service.application.common.exceptions.user import UserIsNotFoundError
from app.access_service.application.common.gateway import UserReader, UserSaver
from app.access_service.application.common.interactor import Interactor
from app.access_service.application.common.uow import UoW
from app.access_service.application.dto import UserConfirmationTokenDTO
from app.access_service.domain.common.entities.timed_token import TimedTokenMetadata
from app.access_service.domain.common.value_objects.timed_token_id import TimedTokenId
from app.access_service.domain.entities.confirmation_token import UserConfirmationToken
from app.access_service.domain.value_objects.expires_in import ExpiresIn
from app.access_service.domain.value_objects.user_id import UserId


class VerifyEmail(Interactor[UserConfirmationTokenDTO, None]):
    def __init__(
        self,
        user_saver: UserSaver,
        user_reader: UserReader,
        uow: UoW,
    ):
        self.user_saver = user_saver
        self.user_reader = user_reader
        self.uow = uow

    async def __call__(self, data: UserConfirmationTokenDTO) -> None:
        metadata = TimedTokenMetadata(uid=UserId(data.uid), expires_in=ExpiresIn(data.expires_in))
        token = UserConfirmationToken(
            metadata=metadata, token_id=TimedTokenId(data.token_id)
        )

        user = await self.user_reader.with_id(token.uid)

        if not user:
            raise UserIsNotFoundError

        user.activate(token)

        await self.user_saver.save_user(user)
        await self.uow.commit()
