from email.message import EmailMessage

import aiosmtplib
from core.domain.model.patient.errors import PatientNotNotified
from core.domain.model.patient.patient_notifier import PatientNotifier
from core.domain.model.patient.patient_query_repository import PatientDto

WELCOME_SUBJECT = "Te damos la bienvenida a la clínica"
WELCOME_BODY = "Hola {first_name}, tu alta como paciente se ha completado."


class EmailPatientNotifier(PatientNotifier):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        sender: str,
        validate_certs: bool = True,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._sender = sender
        self._validate_certs = validate_certs

    async def welcome(self, patient: PatientDto) -> None:
        await self._send(
            patient=patient,
            subject=WELCOME_SUBJECT,
            body=WELCOME_BODY.format(first_name=patient.first_name),
        )

    async def _send(self, patient: PatientDto, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self._sender
        message["To"] = patient.email
        message["Subject"] = subject
        message.set_content(body)
        try:
            await aiosmtplib.send(
                message,
                hostname=self._host,
                port=self._port,
                username=self._username,
                password=self._password,
                validate_certs=self._validate_certs,
            )
        except aiosmtplib.SMTPException as error:
            raise PatientNotNotified(id=patient.id) from error
