from abc import ABC, abstractmethod


class Query[TResult]: ...


class QueryHandler[TQuery: Query, TResult](ABC):
    @abstractmethod
    def handle(self, query: TQuery) -> TResult: ...


class QueryBus(ABC):
    @abstractmethod
    def handle[TResult](self, query: Query[TResult]) -> TResult: ...
