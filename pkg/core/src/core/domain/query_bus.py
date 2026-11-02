from abc import ABC, abstractmethod
from typing import Any


class Query[TResult]: ...


class QueryHandler[TQuery: Query[Any], TResult](ABC):
    @abstractmethod
    async def handle(self, query: TQuery) -> TResult: ...


class QueryBus(ABC):
    @abstractmethod
    async def handle[TResult](self, query: Query[TResult]) -> TResult: ...
