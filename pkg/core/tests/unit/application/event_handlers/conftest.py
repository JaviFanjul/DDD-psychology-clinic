from datetime import UTC, datetime

import pytest
from core.application.event_handlers.bid_farewell_to_patient_on_patient_discharged import (
    BidFarewellToPatientOnPatientDischarged,
)
from core.application.event_handlers.cancel_pending_appointments_on_patient_discharged import (
    CancelPendingAppointmentsOnPatientDischarged,
)
from core.application.event_handlers.welcome_patient_back_on_patient_readmitted import (
    WelcomePatientBackOnPatientReadmitted,
)
from core.application.event_handlers.welcome_patient_on_patient_created import (
    WelcomePatientOnPatientCreated,
)
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_command_repository import (
    AppointmentCommandRepository,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_query_repository import (
    AppointmentDto,
    AppointmentQueryRepository,
)
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_notifier import PatientNotifier
from core.domain.model.patient.patient_query_repository import (
    PatientDto,
    PatientQueryRepository,
)
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_notifier import PsychologistNotifier
from core.domain.model.psychologist.psychologist_query_repository import (
    PsychologistDto,
    PsychologistQueryRepository,
)

KNOWN_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


class StubPatientQueryRepository(PatientQueryRepository):
    def __init__(self, patients: dict[PatientId, PatientDto]) -> None:
        self._patients = patients

    async def find_by_id(self, id: PatientId) -> PatientDto | None:
        return self._patients.get(id)


class SpyPatientNotifier(PatientNotifier):
    def __init__(self) -> None:
        self.welcomed: list[PatientDto] = []
        self.welcomed_back: list[PatientDto] = []
        self.farewelled: list[PatientDto] = []
        self.notified: list[tuple[str, PatientDto, AppointmentDto]] = []

    async def welcome(self, patient: PatientDto) -> None:
        self.welcomed.append(patient)

    async def welcome_back(self, patient: PatientDto) -> None:
        self.welcomed_back.append(patient)

    async def farewell(self, patient: PatientDto) -> None:
        self.farewelled.append(patient)

    async def appointment_scheduled(self, patient: PatientDto, appointment: AppointmentDto) -> None:
        self.notified.append(("appointment_scheduled", patient, appointment))

    async def appointment_rescheduled(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None:
        self.notified.append(("appointment_rescheduled", patient, appointment))

    async def appointment_modality_changed(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None:
        self.notified.append(("appointment_modality_changed", patient, appointment))

    async def appointment_cancelled(self, patient: PatientDto, appointment: AppointmentDto) -> None:
        self.notified.append(("appointment_cancelled", patient, appointment))

    async def request_feedback(self, patient: PatientDto, appointment: AppointmentDto) -> None:
        self.notified.append(("request_feedback", patient, appointment))


class SpyPsychologistNotifier(PsychologistNotifier):
    def __init__(self) -> None:
        self.notified: list[tuple[str, PsychologistDto, AppointmentDto]] = []

    async def appointment_scheduled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        self.notified.append(("appointment_scheduled", psychologist, appointment))

    async def appointment_rescheduled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        self.notified.append(("appointment_rescheduled", psychologist, appointment))

    async def appointment_modality_changed(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        self.notified.append(("appointment_modality_changed", psychologist, appointment))

    async def appointment_cancelled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        self.notified.append(("appointment_cancelled", psychologist, appointment))


class StubAppointmentQueryRepository(AppointmentQueryRepository):
    def __init__(self, appointments: list[AppointmentDto]) -> None:
        self._appointments = {
            AppointmentId.from_string(id=appointment.id): appointment
            for appointment in appointments
        }

    async def find_by_id(self, id: AppointmentId) -> AppointmentDto | None:
        return self._appointments.get(id)

    async def find_pending_slots(
        self, psychologist_id: PsychologistId, excluding: AppointmentId
    ) -> list[AppointmentSlot]:
        return []


class StubPsychologistQueryRepository(PsychologistQueryRepository):
    def __init__(self, psychologists: list[PsychologistDto]) -> None:
        self._psychologists = {
            PsychologistId.from_string(id=psychologist.id): psychologist
            for psychologist in psychologists
        }

    async def find_by_id(self, id: PsychologistId) -> PsychologistDto | None:
        return self._psychologists.get(id)


class SpyAppointmentCommandRepository(AppointmentCommandRepository):
    def __init__(self, appointments: list[Appointment]) -> None:
        self._appointments = appointments
        self.saved: list[Appointment] = []

    async def save(self, appointment: Appointment) -> None:
        self.saved.append(appointment)

    async def find_by_id(self, id: AppointmentId) -> Appointment | None:
        return None

    async def find_pending_by_patient(self, patient_id: PatientId) -> list[Appointment]:
        return [
            appointment
            for appointment in self._appointments
            if appointment.patient_id == patient_id
            and appointment.status is AppointmentStatus.PENDING
        ]


class SpyEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[DomainEvent] = []

    async def publish(self, events: list[DomainEvent]) -> None:
        self.published.extend(events)


@pytest.fixture
def known_id() -> PatientId:
    return PatientId.from_string(id=KNOWN_ID)


@pytest.fixture
def known_patient() -> PatientDto:
    return PatientDto(
        id=KNOWN_ID,
        email="ana@gmail.com",
        first_name="Ana",
        last_names="García López",
        phone_prefix="+34",
        phone_number="612345678",
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
        status="active",
    )


@pytest.fixture
def notifier() -> SpyPatientNotifier:
    return SpyPatientNotifier()


@pytest.fixture
def repository(known_id: PatientId, known_patient: PatientDto) -> StubPatientQueryRepository:
    return StubPatientQueryRepository(patients={known_id: known_patient})


@pytest.fixture
def handler(
    repository: StubPatientQueryRepository, notifier: SpyPatientNotifier
) -> WelcomePatientOnPatientCreated:
    return WelcomePatientOnPatientCreated(repository=repository, notifier=notifier)


@pytest.fixture
def farewell_handler(
    repository: StubPatientQueryRepository, notifier: SpyPatientNotifier
) -> BidFarewellToPatientOnPatientDischarged:
    return BidFarewellToPatientOnPatientDischarged(repository=repository, notifier=notifier)


@pytest.fixture
def welcome_back_handler(
    repository: StubPatientQueryRepository, notifier: SpyPatientNotifier
) -> WelcomePatientBackOnPatientReadmitted:
    return WelcomePatientBackOnPatientReadmitted(repository=repository, notifier=notifier)


KNOWN_PSYCHOLOGIST_ID = "0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
KNOWN_APPOINTMENT_ID = "3f2504e0-4f89-41d3-9a0c-0305e82c3301"
ORPHAN_APPOINTMENT_ID = "9a8b7c6d-5e4f-4a3b-8c2d-1e0f9a8b7c6d"


@pytest.fixture
def known_psychologist() -> PsychologistDto:
    return PsychologistDto(
        id=KNOWN_PSYCHOLOGIST_ID,
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )


def appointment_dto(id: str, patient_id: str, psychologist_id: str) -> AppointmentDto:
    return AppointmentDto(
        id=id,
        patient_id=patient_id,
        psychologist_id=psychologist_id,
        starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC),
        duration_minutes=50,
        modality="in_person",
        status="pending",
    )


@pytest.fixture
def known_appointment() -> AppointmentDto:
    return appointment_dto(
        id=KNOWN_APPOINTMENT_ID, patient_id=KNOWN_ID, psychologist_id=KNOWN_PSYCHOLOGIST_ID
    )


@pytest.fixture
def known_appointment_id() -> AppointmentId:
    return AppointmentId.from_string(id=KNOWN_APPOINTMENT_ID)


@pytest.fixture
def orphan_appointment_id() -> AppointmentId:
    return AppointmentId.from_string(id=ORPHAN_APPOINTMENT_ID)


@pytest.fixture
def appointments(known_appointment: AppointmentDto) -> StubAppointmentQueryRepository:
    orphan_appointment = appointment_dto(
        id=ORPHAN_APPOINTMENT_ID,
        patient_id=str(PatientId.generate()),
        psychologist_id=str(PsychologistId.generate()),
    )
    return StubAppointmentQueryRepository(appointments=[known_appointment, orphan_appointment])


@pytest.fixture
def psychologists(known_psychologist: PsychologistDto) -> StubPsychologistQueryRepository:
    return StubPsychologistQueryRepository(psychologists=[known_psychologist])


@pytest.fixture
def psychologist_notifier() -> SpyPsychologistNotifier:
    return SpyPsychologistNotifier()


@pytest.fixture
def event_bus() -> SpyEventBus:
    return SpyEventBus()


def stored_appointment(patient_id: PatientId, status: AppointmentStatus) -> Appointment:
    return Appointment(
        id=AppointmentId.generate(),
        patient_id=patient_id,
        psychologist_id=PsychologistId.generate(),
        slot=AppointmentSlot(
            starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC),
            duration_minutes=50,
        ),
        modality=AppointmentModality.IN_PERSON,
        status=status,
    )


@pytest.fixture
def pending_appointments(known_id: PatientId) -> list[Appointment]:
    return [
        stored_appointment(patient_id=known_id, status=AppointmentStatus.PENDING),
        stored_appointment(patient_id=known_id, status=AppointmentStatus.PENDING),
    ]


@pytest.fixture
def appointment_repository(
    known_id: PatientId, pending_appointments: list[Appointment]
) -> SpyAppointmentCommandRepository:
    return SpyAppointmentCommandRepository(
        appointments=[
            *pending_appointments,
            stored_appointment(patient_id=known_id, status=AppointmentStatus.COMPLETED),
            stored_appointment(patient_id=PatientId.generate(), status=AppointmentStatus.PENDING),
        ]
    )


@pytest.fixture
def cancel_pending_appointments_handler(
    appointment_repository: SpyAppointmentCommandRepository, event_bus: SpyEventBus
) -> CancelPendingAppointmentsOnPatientDischarged:
    return CancelPendingAppointmentsOnPatientDischarged(
        repository=appointment_repository, event_bus=event_bus
    )
