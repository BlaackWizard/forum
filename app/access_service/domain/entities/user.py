from dataclasses import dataclass

from app.access_service.domain.entities.confirmation_token import UserConfirmationToken
from app.access_service.domain.exceptions.token import CorruptedConfirmationTokenError
from app.access_service.domain.exceptions.user import PasswordMismatchError, InvalidCredentials, \
    UserIsAlreadyActiveError, UserIsNotActiveError
from app.access_service.domain.services.password_hasher import PasswordHasher
from app.access_service.domain.value_objects.user_email import UserEmail
from app.access_service.domain.value_objects.user_hashed_password import UserHashedPassword
from app.access_service.domain.value_objects.user_id import UserId
from app.access_service.domain.value_objects.user_name import UserName
from app.access_service.domain.value_objects.user_raw_password import UserRawPassword


@dataclass
class UserEntity:
    user_id: UserId
    email: UserEmail
    username: UserName
    hashed_password: UserHashedPassword
    is_active: bool = False

    @classmethod
    def create_with_raw_password(
        cls,
        user_id: UserId,
        email: UserEmail,
        username: UserName,
        raw_password: UserRawPassword,
        password_hasher: PasswordHasher
    ) -> "UserEntity":
        hashed_password = password_hasher.hash_password(raw_password)
        return cls(
            user_id=user_id,
            email=email,
            username=username,
            hashed_password=hashed_password
        )
    def __hash__(self):
        return hash(self.user_id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.user_id == other.user_id

    def authenticate(self, raw_password: UserRawPassword, password_hasher: PasswordHasher):
        try:
            password_hasher.verify_password(
                raw_password=raw_password,
                hashed_password=self.hashed_password
            )
        except PasswordMismatchError as exc:
            raise InvalidCredentials from exc

    def ensure_is_active(self):
        if not self.is_active:
            raise UserIsNotActiveError

    def activate(self, token: UserConfirmationToken):
        token.verify()

        if self.is_active:
            raise UserIsAlreadyActiveError

        if self.user_id != token.metadata.uid:
            raise CorruptedConfirmationTokenError

        self._activate()

    def _activate(self):
        self.is_active = True