from datetime import UTC, datetime

import pytest
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_query_repository import (
    AppointmentDto,
    AppointmentQueryRepository,
)
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.psychologist_id import PsychologistId


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


@pytest.fixture
def appointment_id() -> AppointmentId:
    return AppointmentId.generate()


@pytest.fixture
def patient_id() -> PatientId:
    return PatientId.generate()


@pytest.fixture
def psychologist_id() -> PsychologistId:
    return PsychologistId.generate()


@pytest.fixture
def slot() -> AppointmentSlot:
    return AppointmentSlot(starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC), duration_minutes=50)


@pytest.fixture
def other_slot() -> AppointmentSlot:
    return AppointmentSlot(starts_at=datetime(year=2026, month=11, day=12, hour=16, tzinfo=UTC), duration_minutes=60)


@pytest.fixture
def scheduled_appointment(
    appointment_id: AppointmentId,
    patient_id: PatientId,
    psychologist_id: PsychologistId,
    slot: AppointmentSlot,
) -> Appointment:
    return Appointment.schedule(
        id=appointment_id,
        patient_id=patient_id,
        psychologist_id=psychologist_id,
        slot=slot,
        modality=AppointmentModality.IN_PERSON,
    )


@pytest.fixture
def free_agenda() -> StubAppointmentQueryRepository:
    return StubAppointmentQueryRepository(pending_slots=[])


@pytest.fixture
def busy_agenda(slot: AppointmentSlot, other_slot: AppointmentSlot) -> StubAppointmentQueryRepository:
    return StubAppointmentQueryRepository(pending_slots=[other_slot, slot])


@pytest.fixture
def agenda_without_conflicts(other_slot: AppointmentSlot) -> StubAppointmentQueryRepository:
    return StubAppointmentQueryRepository(pending_slots=[other_slot])
