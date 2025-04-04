from app.access_service.domain.exceptions.base import DomainError


class AccessTokenIsExpiredError(DomainError): ...

class ConfirmationTokenIsExpiredError(DomainError): ...

class CorruptedConfirmationTokenError(DomainError): ...