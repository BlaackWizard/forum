from typing import Any, TypeVar, Generic
from abc import abstractmethod

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Interactor(Generic[InputDTO, OutputDTO]):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO: ...
