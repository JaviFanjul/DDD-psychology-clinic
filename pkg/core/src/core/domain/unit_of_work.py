from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from core.domain.domain_error import DomainError


class UnitOfWorkNotCommitted(DomainError):
    def __init__(self) -> None:
        super().__init__("The unit of work could not be committed")


class UnitOfWork(ABC):
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
