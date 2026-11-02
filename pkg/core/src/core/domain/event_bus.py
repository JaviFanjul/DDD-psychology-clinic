from abc import ABC, abstractmethod

from core.domain.domain_event import DomainEvent


class EventHandler[TEvent: DomainEvent](ABC):
    @abstractmethod
    async def handle(self, event: TEvent) -> None: ...


class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None: ...
