from datetime import UTC, datetime

import pytest
from core.application.appointment.command.cancel_appointment import CancelAppointmentCommandHandler
from core.application.appointment.command.change_appointment_modality import (
    ChangeAppointmentModalityCommandHandler,
)
from core.application.appointment.command.complete_appointment import (
    CompleteAppointmentCommandHandler,
)
from core.application.appointment.command.reschedule_appointment import (
    RescheduleAppointmentCommandHandler,
)
from core.application.appointment.command.schedule_appointment import (
    ScheduleAppointmentCommandHandler,
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
from core.domain.model.appointment.psychologist_availability import PsychologistAvailability
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_query_repository import PatientDto, PatientQueryRepository
from core.domain.model.patient.patient_status import PatientStatus
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_query_repository import (
    PsychologistDto,
    PsychologistQueryRepository,
)


class SpyEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[DomainEvent] = []

    async def publish(self, events: list[DomainEvent]) -> None:
        self.published.extend(events)


@pytest.fixture
def event_bus() -> SpyEventBus:
    return SpyEventBus()


class SpyAppointmentCommandRepository(AppointmentCommandRepository):
    def __init__(self, appointments: list[Appointment]) -> None:
        self._appointments = {appointment.id: appointment for appointment in appointments}
        self.saved: list[Appointment] = []

    async def save(self, appointment: Appointment) -> None:
        self.saved.append(appointment)

    async def find_by_id(self, id: AppointmentId) -> Appointment | None:
        return self._appointments.get(id)

    async def find_pending_by_patient(self, patient_id: PatientId) -> list[Appointment]:
        return []


class StubAppointmentQueryRepository(AppointmentQueryRepository):
    def __init__(self, pending_slots: list[AppointmentSlot]) -> None:
        self._pending_slots = pending_slots
        self.slot_queries: list[tuple[PsychologistId, AppointmentId]] = []

    async def find_by_id(self, id: AppointmentId) -> AppointmentDto | None:
        return None

    async def find_pending_slots(
        self, psychologist_id: PsychologistId, excluding: AppointmentId
    ) -> list[AppointmentSlot]:
        self.slot_queries.append((psychologist_id, excluding))
        return self._pending_slots


class StubPatientQueryRepository(PatientQueryRepository):
    def __init__(self, patients: list[PatientDto]) -> None:
        self._patients = {PatientId.from_string(id=patient.id): patient for patient in patients}

    async def find_by_id(self, id: PatientId) -> PatientDto | None:
        return self._patients.get(id)


class StubPsychologistQueryRepository(PsychologistQueryRepository):
    def __init__(self, psychologists: list[PsychologistDto]) -> None:
        self._psychologists = {
            PsychologistId.from_string(id=psychologist.id): psychologist for psychologist in psychologists
        }

    async def find_by_id(self, id: PsychologistId) -> PsychologistDto | None:
        return self._psychologists.get(id)


def patient_dto(id: str, status: PatientStatus) -> PatientDto:
    return PatientDto(
        id=id,
        email="ana@gmail.com",
        first_name="Ana",
        last_names="García López",
        phone_prefix="+34",
        phone_number="612345678",
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
        status=status.value,
    )


@pytest.fixture
def active_patient_dto() -> PatientDto:
    return patient_dto(id="7c9e6679-7425-40de-944b-e07fc1f90ae7", status=PatientStatus.ACTIVE)


@pytest.fixture
def discharged_patient_dto() -> PatientDto:
    return patient_dto(id="1b4e28ba-2fa1-41d2-883f-0016d3cca427", status=PatientStatus.DISCHARGED)


@pytest.fixture
def psychologist_dto() -> PsychologistDto:
    return PsychologistDto(
        id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )


@pytest.fixture
def slot() -> AppointmentSlot:
    return AppointmentSlot(starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC), duration_minutes=50)


@pytest.fixture
def other_slot() -> AppointmentSlot:
    return AppointmentSlot(starts_at=datetime(year=2026, month=11, day=12, hour=16, tzinfo=UTC), duration_minutes=60)


def stored_appointment(status: AppointmentStatus, slot: AppointmentSlot) -> Appointment:
    return Appointment(
        id=AppointmentId.generate(),
        patient_id=PatientId.generate(),
        psychologist_id=PsychologistId.generate(),
        slot=slot,
        modality=AppointmentModality.IN_PERSON,
        status=status,
    )


@pytest.fixture
def pending_appointment(slot: AppointmentSlot) -> Appointment:
    return stored_appointment(status=AppointmentStatus.PENDING, slot=slot)


@pytest.fixture
def cancelled_appointment(slot: AppointmentSlot) -> Appointment:
    return stored_appointment(status=AppointmentStatus.CANCELLED, slot=slot)


@pytest.fixture
def appointment_repository(
    pending_appointment: Appointment, cancelled_appointment: Appointment
) -> SpyAppointmentCommandRepository:
    return SpyAppointmentCommandRepository(appointments=[pending_appointment, cancelled_appointment])


@pytest.fixture
def free_agenda() -> StubAppointmentQueryRepository:
    return StubAppointmentQueryRepository(pending_slots=[])


@pytest.fixture
def busy_agenda(slot: AppointmentSlot, other_slot: AppointmentSlot) -> StubAppointmentQueryRepository:
    return StubAppointmentQueryRepository(pending_slots=[slot, other_slot])


@pytest.fixture
def patient_query_repository(
    active_patient_dto: PatientDto, discharged_patient_dto: PatientDto
) -> StubPatientQueryRepository:
    return StubPatientQueryRepository(patients=[active_patient_dto, discharged_patient_dto])


@pytest.fixture
def psychologist_query_repository(
    psychologist_dto: PsychologistDto,
) -> StubPsychologistQueryRepository:
    return StubPsychologistQueryRepository(psychologists=[psychologist_dto])


def schedule_handler(
    appointment_repository: SpyAppointmentCommandRepository,
    agenda: StubAppointmentQueryRepository,
    patient_query_repository: StubPatientQueryRepository,
    psychologist_query_repository: StubPsychologistQueryRepository,
    event_bus: SpyEventBus,
) -> ScheduleAppointmentCommandHandler:
    return ScheduleAppointmentCommandHandler(
        repository=appointment_repository,
        availability=PsychologistAvailability(repository=agenda),
        patients=patient_query_repository,
        psychologists=psychologist_query_repository,
        event_bus=event_bus,
    )


@pytest.fixture
def schedule_appointment_handler(
    appointment_repository: SpyAppointmentCommandRepository,
    free_agenda: StubAppointmentQueryRepository,
    patient_query_repository: StubPatientQueryRepository,
    psychologist_query_repository: StubPsychologistQueryRepository,
    event_bus: SpyEventBus,
) -> ScheduleAppointmentCommandHandler:
    return schedule_handler(
        appointment_repository=appointment_repository,
        agenda=free_agenda,
        patient_query_repository=patient_query_repository,
        psychologist_query_repository=psychologist_query_repository,
        event_bus=event_bus,
    )


@pytest.fixture
def schedule_appointment_handler_with_busy_agenda(
    appointment_repository: SpyAppointmentCommandRepository,
    busy_agenda: StubAppointmentQueryRepository,
    patient_query_repository: StubPatientQueryRepository,
    psychologist_query_repository: StubPsychologistQueryRepository,
    event_bus: SpyEventBus,
) -> ScheduleAppointmentCommandHandler:
    return schedule_handler(
        appointment_repository=appointment_repository,
        agenda=busy_agenda,
        patient_query_repository=patient_query_repository,
        psychologist_query_repository=psychologist_query_repository,
        event_bus=event_bus,
    )


@pytest.fixture
def reschedule_appointment_handler(
    appointment_repository: SpyAppointmentCommandRepository,
    free_agenda: StubAppointmentQueryRepository,
    event_bus: SpyEventBus,
) -> RescheduleAppointmentCommandHandler:
    return RescheduleAppointmentCommandHandler(
        repository=appointment_repository,
        availability=PsychologistAvailability(repository=free_agenda),
        event_bus=event_bus,
    )


@pytest.fixture
def reschedule_appointment_handler_with_busy_agenda(
    appointment_repository: SpyAppointmentCommandRepository,
    busy_agenda: StubAppointmentQueryRepository,
    event_bus: SpyEventBus,
) -> RescheduleAppointmentCommandHandler:
    return RescheduleAppointmentCommandHandler(
        repository=appointment_repository,
        availability=PsychologistAvailability(repository=busy_agenda),
        event_bus=event_bus,
    )


@pytest.fixture
def change_appointment_modality_handler(
    appointment_repository: SpyAppointmentCommandRepository, event_bus: SpyEventBus
) -> ChangeAppointmentModalityCommandHandler:
    return ChangeAppointmentModalityCommandHandler(repository=appointment_repository, event_bus=event_bus)


@pytest.fixture
def cancel_appointment_handler(
    appointment_repository: SpyAppointmentCommandRepository, event_bus: SpyEventBus
) -> CancelAppointmentCommandHandler:
    return CancelAppointmentCommandHandler(repository=appointment_repository, event_bus=event_bus)


@pytest.fixture
def complete_appointment_handler(
    appointment_repository: SpyAppointmentCommandRepository, event_bus: SpyEventBus
) -> CompleteAppointmentCommandHandler:
    return CompleteAppointmentCommandHandler(repository=appointment_repository, event_bus=event_bus)
