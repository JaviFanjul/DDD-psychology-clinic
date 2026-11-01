import pytest
from core.application.command.register_patient import RegisterPatientCommandHandler
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_id import PatientId


class SpyPatientCommandRepository(PatientCommandRepository):
    def __init__(self) -> None:
        self.saved: list[Patient] = []

    def save(self, patient: Patient) -> None:
        self.saved.append(patient)

    def find_by_id(self, id: PatientId) -> Patient | None:
        return None


class SpyEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[DomainEvent] = []

    def publish(self, events: list[DomainEvent]) -> None:
        self.published.extend(events)


@pytest.fixture
def repository() -> SpyPatientCommandRepository:
    return SpyPatientCommandRepository()


@pytest.fixture
def event_bus() -> SpyEventBus:
    return SpyEventBus()


@pytest.fixture
def handler(
    repository: SpyPatientCommandRepository, event_bus: SpyEventBus
) -> RegisterPatientCommandHandler:
    return RegisterPatientCommandHandler(repository, event_bus)
