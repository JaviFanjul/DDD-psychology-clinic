from datetime import UTC, datetime

import pytest
from core.domain.domain_event import DomainEvent
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.psychologist_id import PsychologistId


class UnknownEvent(DomainEvent): ...


@pytest.fixture
def patient_id() -> PatientId:
    return PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7")


@pytest.fixture
def psychologist_id() -> PsychologistId:
    return PsychologistId.from_string(id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d")


@pytest.fixture
def created_at() -> datetime:
    return datetime(year=2026, month=11, day=2, hour=10, minute=30, tzinfo=UTC)


@pytest.fixture
def unknown_event() -> UnknownEvent:
    return UnknownEvent()
