import aiosmtplib
import pytest
from core.domain.model.patient.patient_query_repository import PatientDto
from core.infrastructure.email.email_patient_notifier import EmailPatientNotifier


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
