import pytest
from core.application.patient.command.create_patient import CreatePatientCommandHandler
from core.application.patient.command.discharge_patient import DischargePatientCommandHandler
from core.application.patient.command.readmit_patient import ReadmitPatientCommandHandler
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone
from core.domain.model.patient.patient_status import PatientStatus


class SpyPatientCommandRepository(PatientCommandRepository):
    def __init__(self, patients: list[Patient]) -> None:
        self._patients = {patient.id: patient for patient in patients}
        self.saved: list[Patient] = []

    async def save(self, patient: Patient) -> None:
        self.saved.append(patient)

    async def find_by_id(self, id: PatientId) -> Patient | None:
        return self._patients.get(id)


class SpyEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[DomainEvent] = []

    async def publish(self, events: list[DomainEvent]) -> None:
        self.published.extend(events)


@pytest.fixture
def patient_name() -> PatientName:
    return PatientName(first_name="Ana", last_names="García López")


@pytest.fixture
def patient_phone() -> PatientPhone:
    return PatientPhone(prefix="+34", number="612345678")


@pytest.fixture
def patient_address() -> PatientAddress:
    return PatientAddress(
        street="Calle Mayor 3, 2º B", postal_code="08001", city="Barcelona", province="Barcelona"
    )


def stored_patient(
    status: PatientStatus,
    name: PatientName,
    phone: PatientPhone,
    address: PatientAddress,
) -> Patient:
    return Patient(
        id=PatientId.generate(),
        email=PatientEmail(value="ana@gmail.com"),
        name=name,
        phone=phone,
        address=address,
        status=status,
    )


@pytest.fixture
def active_patient(
    patient_name: PatientName, patient_phone: PatientPhone, patient_address: PatientAddress
) -> Patient:
    return stored_patient(
        status=PatientStatus.ACTIVE, name=patient_name, phone=patient_phone, address=patient_address
    )


@pytest.fixture
def discharged_patient(
    patient_name: PatientName, patient_phone: PatientPhone, patient_address: PatientAddress
) -> Patient:
    return stored_patient(
        status=PatientStatus.DISCHARGED,
        name=patient_name,
        phone=patient_phone,
        address=patient_address,
    )


@pytest.fixture
def repository(active_patient: Patient, discharged_patient: Patient) -> SpyPatientCommandRepository:
    return SpyPatientCommandRepository(patients=[active_patient, discharged_patient])


@pytest.fixture
def event_bus() -> SpyEventBus:
    return SpyEventBus()


@pytest.fixture
def handler(
    repository: SpyPatientCommandRepository, event_bus: SpyEventBus
) -> CreatePatientCommandHandler:
    return CreatePatientCommandHandler(repository=repository, event_bus=event_bus)


@pytest.fixture
def discharge_handler(
    repository: SpyPatientCommandRepository, event_bus: SpyEventBus
) -> DischargePatientCommandHandler:
    return DischargePatientCommandHandler(repository=repository, event_bus=event_bus)


@pytest.fixture
def readmit_handler(
    repository: SpyPatientCommandRepository, event_bus: SpyEventBus
) -> ReadmitPatientCommandHandler:
    return ReadmitPatientCommandHandler(repository=repository, event_bus=event_bus)
