import pytest
from core.application.command.create_patient import CreatePatientCommandHandler
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName


class SpyPatientCommandRepository(PatientCommandRepository):
    def __init__(self) -> None:
        self.saved: list[Patient] = []

    async def save(self, patient: Patient) -> None:
        self.saved.append(patient)

    async def find_by_id(self, id: PatientId) -> Patient | None:
        return None


class SpyEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[DomainEvent] = []

    async def publish(self, events: list[DomainEvent]) -> None:
        self.published.extend(events)


@pytest.fixture
def patient_name() -> PatientName:
    return PatientName(first_name="Ana", last_names="García López")


@pytest.fixture
def patient_address() -> PatientAddress:
    return PatientAddress(
        street="Calle Mayor 3, 2º B", postal_code="08001", city="Barcelona", province="Barcelona"
    )


@pytest.fixture
def repository() -> SpyPatientCommandRepository:
    return SpyPatientCommandRepository()


@pytest.fixture
def event_bus() -> SpyEventBus:
    return SpyEventBus()


@pytest.fixture
def handler(
    repository: SpyPatientCommandRepository, event_bus: SpyEventBus
) -> CreatePatientCommandHandler:
    return CreatePatientCommandHandler(repository=repository, event_bus=event_bus)
