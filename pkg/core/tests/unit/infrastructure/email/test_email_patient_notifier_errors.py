import aiosmtplib
import pytest
from core.domain.model.patient.errors import PatientNotNotified


@pytest.mark.parametrize("notification", ["welcome", "welcome_back", "farewell"])
async def test_given_a_failing_smtp_server_when_notifying_then_it_raises_patient_not_notified(
    notifier, patient, notification
):
    with pytest.raises(PatientNotNotified) as raised:
        await getattr(notifier, notification)(patient=patient)

    assert isinstance(raised.value.__cause__, aiosmtplib.SMTPException)


@pytest.mark.parametrize(
    "notification",
    [
        "appointment_scheduled",
        "appointment_rescheduled",
        "appointment_modality_changed",
        "appointment_cancelled",
        "request_feedback",
    ],
)
async def test_given_a_failing_smtp_server_when_notifying_an_appointment_then_it_raises(
    notifier, patient, appointment, notification
):
    with pytest.raises(PatientNotNotified) as raised:
        await getattr(notifier, notification)(patient=patient, appointment=appointment)

    assert isinstance(raised.value.__cause__, aiosmtplib.SMTPException)
