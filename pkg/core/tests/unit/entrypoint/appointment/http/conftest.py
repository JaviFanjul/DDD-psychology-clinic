from datetime import UTC, datetime
from typing import Any

import pytest
from core.domain.command_bus import Command, CommandBus
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.query_bus import Query, QueryBus
from core.entrypoint.appointment.http.appointment_controller import AppointmentController

APPOINTMENT_ID = "3f2504e0-4f89-41d3-9a0c-0305e82c3301"


class SpyCommandBus(CommandBus):
    def __init__(self) -> None:
        self.handled: list[Command] = []

    async def handle(self, command: Command) -> None:
        self.handled.append(command)


class SpyQueryBus(QueryBus):
    def __init__(self, result: AppointmentDto) -> None:
        self._result = result
        self.handled: list[Query] = []

    async def handle[TResult](self, query: Query[TResult]) -> TResult:
        self.handled.append(query)
        return self._result


@pytest.fixture
def starts_at() -> datetime:
    return datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC)


@pytest.fixture
def schedule_data(starts_at: datetime) -> dict[str, Any]:
    return {
        "patient_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "psychologist_id": "0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        "starts_at": starts_at,
        "duration_minutes": 50,
        "modality": "online",
    }


@pytest.fixture
def appointment_dto(starts_at: datetime) -> AppointmentDto:
    return AppointmentDto(
        id=APPOINTMENT_ID,
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        psychologist_id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        starts_at=starts_at,
        duration_minutes=50,
        modality="online",
        status="pending",
    )


@pytest.fixture
def command_bus() -> SpyCommandBus:
    return SpyCommandBus()


@pytest.fixture
def query_bus(appointment_dto: AppointmentDto) -> SpyQueryBus:
    return SpyQueryBus(result=appointment_dto)


@pytest.fixture
def controller(command_bus: SpyCommandBus, query_bus: SpyQueryBus) -> AppointmentController:
    return AppointmentController(command_bus=command_bus, query_bus=query_bus)
