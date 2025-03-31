from abc import ABC, abstractmethod

from app.access_service.domain.value_objects.user_hashed_password import UserHashedPassword
from app.access_service.domain.value_objects.user_raw_password import UserRawPassword


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, raw_password: UserRawPassword) -> UserHashedPassword: ...

    @abstractmethod
    def verify_password(self, hashed_password: UserHashedPassword, raw_password: UserRawPassword) -> bool: ...
