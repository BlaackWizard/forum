from abc import ABC, abstractmethod

from app.access_service.application.dto import UserConfirmationTokenDTO
from app.access_service.domain.entities.user import UserEntity


class TokenSender(ABC):
    @abstractmethod
    async def send(
        self,
        confirmation_token: UserConfirmationTokenDTO,
        user: UserEntity
    ) -> None: ...
