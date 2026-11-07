import pytest


@pytest.mark.parametrize(
    ("notification", "expected_subject", "expected_text"),
    [
        (
            "appointment_scheduled",
            "Tienes una nueva consulta",
            "Hola Laura, tienes una nueva consulta presencial el 10/11/2026 a las 10:00 "
            "(50 minutos).",
        ),
        (
            "appointment_rescheduled",
            "Una consulta ha cambiado de fecha",
            "Hola Laura, tu consulta presencial ahora es el 10/11/2026 a las 10:00 (50 minutos).",
        ),
        (
            "appointment_modality_changed",
            "Una consulta ha cambiado de modalidad",
            "Hola Laura, tu consulta del 10/11/2026 a las 10:00 ahora es presencial.",
        ),
        (
            "appointment_cancelled",
            "Una consulta ha sido cancelada",
            "Hola Laura, tu consulta del 10/11/2026 a las 10:00 ha sido cancelada.",
        ),
    ],
)
async def test_given_an_appointment_when_notifying_the_psychologist_then_the_email_reaches_them(
    psychologist_notifier,
    mailbox,
    psychologist,
    appointment,
    notification,
    expected_subject,
    expected_text,
):
    await getattr(psychologist_notifier, notification)(
        psychologist=psychologist, appointment=appointment
    )

    [message] = mailbox.messages()
    assert message["From"]["Address"] == "clinica@example.com"
    assert [recipient["Address"] for recipient in message["To"]] == ["laura@clinica.es"]
    assert message["Subject"] == expected_subject
    assert message["Text"].strip() == expected_text
