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


@pytest.fixture
def psychologist_repository() -> SpyPsychologistCommandRepository:
    return SpyPsychologistCommandRepository()


@pytest.fixture
def create_psychologist_handler(
    psychologist_repository: SpyPsychologistCommandRepository, event_bus: SpyEventBus
) -> CreatePsychologistCommandHandler:
    return CreatePsychologistCommandHandler(repository=psychologist_repository, event_bus=event_bus)
