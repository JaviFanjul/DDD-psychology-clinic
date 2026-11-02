from collections import defaultdict
from typing import Any

from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus, EventHandler


class InMemoryEventBus(EventBus):
    def __init__(self) -> None:
        self._handlers: defaultdict[type[DomainEvent], list[EventHandler[Any]]] = defaultdict(list)

    def register[TEvent: DomainEvent](
        self, event_type: type[TEvent], handler: EventHandler[TEvent]
    ) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            for handler in self._handlers.get(type(event), []):
                await handler.handle(event=event)
