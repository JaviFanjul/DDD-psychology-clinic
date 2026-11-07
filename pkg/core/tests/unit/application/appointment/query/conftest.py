from datetime import UTC, datetime

import pytest
from core.application.appointment.query.get_appointment import GetAppointmentQueryHandler
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_query_repository import (
    AppointmentDto,
    AppointmentQueryRepository,
)
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.psychologist.psychologist_id import PsychologistId


class StubAppointmentQueryRepository(AppointmentQueryRepository):
    def __init__(self, appointments: dict[AppointmentId, AppointmentDto]) -> None:
        self._appointments = appointments

    async def find_by_id(self, id: AppointmentId) -> AppointmentDto | None:
        return self._appointments.get(id)

    async def find_pending_slots(
        self, psychologist_id: PsychologistId, excluding: AppointmentId
    ) -> list[AppointmentSlot]:
        return []


KNOWN_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


@pytest.fixture
def known_id() -> str:
    return KNOWN_ID


@pytest.fixture
def known_appointment(known_id: str) -> AppointmentDto:
    return AppointmentDto(
        id=known_id,
        patient_id="1b4e28ba-2fa1-41d2-883f-0016d3cca427",
        psychologist_id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC),
        duration_minutes=50,
        modality="online",
        status="pending",
    )


@pytest.fixture
def appointment_handler(
    known_id: str, known_appointment: AppointmentDto
) -> GetAppointmentQueryHandler:
    repository = StubAppointmentQueryRepository(
        appointments={AppointmentId.from_string(id=known_id): known_appointment}
    )
    return GetAppointmentQueryHandler(repository=repository)
