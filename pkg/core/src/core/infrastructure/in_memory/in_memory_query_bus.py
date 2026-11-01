from typing import Any

from core.domain.query_bus import Query, QueryBus, QueryHandler


class InMemoryQueryBus(QueryBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Query[Any]], QueryHandler[Any, Any]] = {}

    def register[TQuery: Query[Any], TResult](
        self, query_type: type[TQuery], handler: QueryHandler[TQuery, TResult]
    ) -> None:
        self._handlers[query_type] = handler

    def handle[TResult](self, query: Query[TResult]) -> TResult:
        result: TResult = self._handlers[type(query)].handle(query=query)
        return result
