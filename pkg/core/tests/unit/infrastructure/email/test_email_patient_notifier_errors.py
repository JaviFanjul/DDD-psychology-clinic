import aiosmtplib
import pytest
from core.domain.model.patient.errors import PatientNotNotified


async def test_given_a_failing_smtp_server_when_welcoming_then_it_raises_patient_not_notified(
    notifier, patient
):
    with pytest.raises(PatientNotNotified) as raised:
        await notifier.welcome(patient=patient)

    assert isinstance(raised.value.__cause__, aiosmtplib.SMTPException)
