import pytest
from core.application.psychologist.command.create_psychologist import (
    CreatePsychologistCommandHandler,
)
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus
from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_command_repository import (
    PsychologistCommandRepository,
)
from core.domain.unit_of_work import UnitOfWork


class SpyPsychologistCommandRepository(PsychologistCommandRepository):
    def __init__(self) -> None:
        self.saved: list[Psychologist] = []

    async def save(self, psychologist: Psychologist) -> None:
        self.saved.append(psychologist)


class SpyEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[DomainEvent] = []

    async def publish(self, events: list[DomainEvent]) -> None:
        self.published.extend(events)


@pytest.fixture
def event_bus() -> SpyEventBus:
    return SpyEventBus()


class SpyUnitOfWork(UnitOfWork):
    def __init__(self, event_bus: SpyEventBus) -> None:
        self._event_bus = event_bus
        self.committed = False
        self.published_before_commit: list[DomainEvent] = []

    async def commit(self) -> None:
        self.committed = True
        self.published_before_commit = list(self._event_bus.published)

    async def rollback(self) -> None: ...


@pytest.fixture
def unit_of_work(event_bus: SpyEventBus) -> SpyUnitOfWork:
    return SpyUnitOfWork(event_bus=event_bus)


@pytest.fixture
def psychologist_repository() -> SpyPsychologistCommandRepository:
    return SpyPsychologistCommandRepository()


@pytest.fixture
def create_psychologist_handler(
    psychologist_repository: SpyPsychologistCommandRepository, unit_of_work: SpyUnitOfWork, event_bus: SpyEventBus
) -> CreatePsychologistCommandHandler:
    return CreatePsychologistCommandHandler(
        repository=psychologist_repository, unit_of_work=unit_of_work, event_bus=event_bus
    )
