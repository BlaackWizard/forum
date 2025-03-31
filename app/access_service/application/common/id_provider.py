from abc import ABC, abstractmethod

from app.access_service.domain.entities.user import UserEntity


class IdProvider(ABC):
    @abstractmethod
    async def get_user(self) -> UserEntity: ...
