from abc import abstractmethod
from typing import Protocol

from app.access_service.domain.entities.user import UserEntity


class AccessService(Protocol):
    @abstractmethod
    def authorize(self, user: UserEntity) -> None: ...
