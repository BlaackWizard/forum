from abc import ABC, abstractmethod

class UoW(ABC):
    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
