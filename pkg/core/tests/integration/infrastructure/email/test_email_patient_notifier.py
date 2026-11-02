async def test_given_a_patient_when_welcoming_them_then_a_welcome_email_reaches_them(
    notifier, mailbox, patient
):
    await notifier.welcome(patient=patient)

    [message] = mailbox.messages()
    assert message["From"]["Address"] == "clinica@example.com"
    assert [recipient["Address"] for recipient in message["To"]] == ["ana@gmail.com"]
    assert message["Subject"] == "Te damos la bienvenida a la clínica"
    assert message["Text"].strip() == "Hola Ana, tu alta como paciente se ha completado."
