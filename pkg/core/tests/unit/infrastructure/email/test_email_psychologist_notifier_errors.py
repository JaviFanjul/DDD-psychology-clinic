import aiosmtplib
import pytest
from core.domain.model.psychologist.errors import PsychologistNotNotified


@pytest.mark.parametrize(
    "notification",
    [
        "appointment_scheduled",
        "appointment_rescheduled",
        "appointment_modality_changed",
        "appointment_cancelled",
    ],
)
async def test_given_a_failing_smtp_server_when_notifying_then_it_raises_psychologist_not_notified(
    psychologist_notifier, psychologist, appointment, notification
):
    with pytest.raises(PsychologistNotNotified) as raised:
        await getattr(psychologist_notifier, notification)(
            psychologist=psychologist, appointment=appointment
        )

    assert isinstance(raised.value.__cause__, aiosmtplib.SMTPException)
