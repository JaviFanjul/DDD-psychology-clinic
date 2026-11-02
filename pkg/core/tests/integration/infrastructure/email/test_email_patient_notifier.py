async def test_given_a_patient_when_welcoming_them_then_a_welcome_email_reaches_them(
    notifier, mailbox, patient
):
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
    assert message["Text"].strip() == (
        "Hola Ana, tu baja como paciente se ha completado. Te deseamos lo mejor."
    )


async def test_given_a_patient_when_welcoming_them_back_then_a_welcome_back_email_reaches_them(
    notifier, mailbox, patient
):
    await notifier.welcome_back(patient=patient)

    [message] = mailbox.messages()
    assert message["From"]["Address"] == "clinica@example.com"
    assert [recipient["Address"] for recipient in message["To"]] == ["ana@gmail.com"]
    assert message["Subject"] == "Te damos la bienvenida de nuevo a la clínica"
    assert message["Text"].strip() == "Hola Ana, nos alegra volver a verte en la clínica."
