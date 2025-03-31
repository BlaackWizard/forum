from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.access_service.domain.common.value_objects.timed_token_id import TimedTokenId
from app.access_service.domain.value_objects.expires_in import ExpiresIn
from app.access_service.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class TimedTokenMetadata:
    uid: UserId
    expires_in: ExpiresIn

@dataclass(frozen=True)
class TimedTokenUser(ABC):
    metadata: TimedTokenMetadata
    token_id: TimedTokenId

    @property
    def uid(self):
        return self.metadata.uid

    @property
    def expires_in(self):
        return self.metadata.expires_in

    @abstractmethod
    def verify(self) -> None: ...
