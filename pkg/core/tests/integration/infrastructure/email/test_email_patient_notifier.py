import pytest


async def test_given_a_patient_when_welcoming_them_then_a_welcome_email_reaches_them(notifier, mailbox, patient):
    await notifier.welcome(patient=patient)

    [message] = mailbox.messages()
    assert message["From"]["Address"] == "clinica@example.com"
    assert [recipient["Address"] for recipient in message["To"]] == ["ana@gmail.com"]
    assert message["Subject"] == "Te damos la bienvenida a la clínica"
    assert message["Text"].strip() == "Hola Ana, tu alta como paciente se ha completado."


async def test_given_a_patient_when_bidding_them_farewell_then_a_farewell_email_reaches_them(
    notifier, mailbox, patient
):
    await notifier.farewell(patient=patient)

    [message] = mailbox.messages()
    assert message["From"]["Address"] == "clinica@example.com"
    assert [recipient["Address"] for recipient in message["To"]] == ["ana@gmail.com"]
    assert message["Subject"] == "Gracias por confiar en la clínica"
    assert message["Text"].strip() == ("Hola Ana, tu baja como paciente se ha completado. Te deseamos lo mejor.")


async def test_given_a_patient_when_welcoming_them_back_then_a_welcome_back_email_reaches_them(
    notifier, mailbox, patient
):
    await notifier.welcome_back(patient=patient)

    [message] = mailbox.messages()
    assert message["From"]["Address"] == "clinica@example.com"
    assert [recipient["Address"] for recipient in message["To"]] == ["ana@gmail.com"]
    assert message["Subject"] == "Te damos la bienvenida de nuevo a la clínica"
    assert message["Text"].strip() == "Hola Ana, nos alegra volver a verte en la clínica."


@pytest.mark.parametrize(
    ("notification", "expected_subject", "expected_text"),
    [
        (
            "appointment_scheduled",
            "Tu consulta ha quedado agendada",
            "Hola Ana, tu consulta presencial del 10/11/2026 a las 10:00 (50 minutos) ha quedado agendada.",
        ),
        (
            "appointment_rescheduled",
            "Tu consulta ha cambiado de fecha",
            "Hola Ana, tu consulta presencial ahora es el 10/11/2026 a las 10:00 (50 minutos).",
        ),
        (
            "appointment_modality_changed",
            "Tu consulta ha cambiado de modalidad",
            "Hola Ana, tu consulta del 10/11/2026 a las 10:00 ahora es presencial.",
        ),
        (
            "appointment_cancelled",
            "Tu consulta ha sido cancelada",
            "Hola Ana, tu consulta del 10/11/2026 a las 10:00 ha sido cancelada.",
        ),
        (
            "request_feedback",
            "¿Qué tal fue tu consulta?",
            "Hola Ana, gracias por venir a tu consulta del 10/11/2026. Nos encantaría saber "
            "qué tal fue: responde a este correo y cuéntanos tu opinión.",
        ),
    ],
)
async def test_given_an_appointment_when_notifying_the_patient_then_its_email_reaches_them(
    notifier, mailbox, patient, appointment, notification, expected_subject, expected_text
):
    await getattr(notifier, notification)(patient=patient, appointment=appointment)

    [message] = mailbox.messages()
    assert message["From"]["Address"] == "clinica@example.com"
    assert [recipient["Address"] for recipient in message["To"]] == ["ana@gmail.com"]
    assert message["Subject"] == expected_subject
    assert message["Text"].strip() == expected_text
