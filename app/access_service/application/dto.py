from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.access_service.application.common.event.event import Event


@dataclass
class AccessTokenDTO:
    uid: UUID
    expires_in: datetime
    token_id: UUID

@dataclass
class UserConfirmationTokenDTO:
    uid: UUID
    expires_in: datetime
    token_id: UUID

@dataclass
class UserDTO:
    user_id: UUID


@dataclass(frozen=True)
class UserDeletedEvent(Event):
    user_id: UUID
