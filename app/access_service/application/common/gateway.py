from abc import ABC, abstractmethod

from app.access_service.application.dto import UserDTO
from app.access_service.domain.entities.user import UserEntity
from app.access_service.domain.value_objects.user_email import UserEmail
from app.access_service.domain.value_objects.user_id import UserId


class UserReader(ABC):
    @abstractmethod
    async def with_email(self, email: UserEmail) -> UserEntity | None: ...

    @abstractmethod
    async def with_id(self, user_id: UserId) -> UserEntity | None: ...

class UserSaver(ABC):
    @abstractmethod
    async def save_user(self, user: UserEntity) -> UserDTO: ...

    @abstractmethod
    async def delete_user(self, user_id: UserId) -> None: ...
