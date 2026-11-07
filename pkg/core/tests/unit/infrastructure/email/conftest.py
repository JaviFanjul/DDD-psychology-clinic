from datetime import UTC, datetime

import aiosmtplib
import pytest
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.patient.patient_query_repository import PatientDto
from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto
from core.infrastructure.email.email_patient_notifier import EmailPatientNotifier
from core.infrastructure.email.email_psychologist_notifier import EmailPsychologistNotifier


async def failing_send(*args, **kwargs):
    raise aiosmtplib.SMTPConnectError("SMTP server unavailable")


@pytest.fixture
def notifier(monkeypatch: pytest.MonkeyPatch) -> EmailPatientNotifier:
    monkeypatch.setattr(aiosmtplib, "send", failing_send)
    return EmailPatientNotifier(
        host="smtp.example.com",
        port=587,
        username="clinica",
        password="secret",
        sender="clinica@example.com",
    )


@pytest.fixture
def patient() -> PatientDto:
    return PatientDto(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
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
def psychologist_notifier(monkeypatch: pytest.MonkeyPatch) -> EmailPsychologistNotifier:
    monkeypatch.setattr(aiosmtplib, "send", failing_send)
    return EmailPsychologistNotifier(
        host="smtp.example.com",
        port=587,
        username="clinica",
        password="secret",
        sender="clinica@example.com",
    )


@pytest.fixture
def psychologist() -> PsychologistDto:
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
def appointment() -> AppointmentDto:
    return AppointmentDto(
        id="3f2504e0-4f89-41d3-9a0c-0305e82c3301",
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        psychologist_id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC),
        duration_minutes=50,
        modality="online",
        status="pending",
    )
