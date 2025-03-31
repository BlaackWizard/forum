from app.access_service.application.common.event.event_emitter import EventEmitter
from app.access_service.application.common.gateway import UserSaver
from app.access_service.application.common.id_provider import IdProvider
from app.access_service.application.common.interactor import Interactor
from dataclasses import dataclass

from app.access_service.application.dto import UserDeletedEvent
from app.access_service.domain.services.password_hasher import PasswordHasher
from app.access_service.domain.value_objects.user_raw_password import UserRawPassword


@dataclass
class DeleteUserDTO:
    password: str

class DeleteUser(Interactor[DeleteUserDTO, None]):
    def __init__(
        self,
        id_provider: IdProvider,
        user_gateway: UserSaver,
        ph: PasswordHasher,
        event_emitter: EventEmitter[UserDeletedEvent]
    ):
        self.id_provider = id_provider
        self.user_gateway = user_gateway
        self.ph = ph
        self.event_emitter = event_emitter

    async def __call__(self, data: DeleteUserDTO) -> None:
        user = await self.id_provider.get_user()
        raw_password = UserRawPassword(data.password)

        user.authenticate(raw_password, self.ph)
        await self.user_gateway.delete_user(user.user_id)

        event = UserDeletedEvent(user_id=user.user_id.to_raw())

        await self.event_emitter.emit(event)
