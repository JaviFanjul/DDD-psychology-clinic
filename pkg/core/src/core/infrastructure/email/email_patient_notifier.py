from email.message import EmailMessage

import aiosmtplib
from core.domain.model.patient.errors import PatientNotNotified
from core.domain.model.patient.patient_notifier import PatientNotifier
from core.domain.model.patient.patient_query_repository import PatientDto

WELCOME_SUBJECT = "Te damos la bienvenida a la clínica"
WELCOME_BODY = "Hola {first_name}, tu alta como paciente se ha completado."
WELCOME_BACK_SUBJECT = "Te damos la bienvenida de nuevo a la clínica"
WELCOME_BACK_BODY = "Hola {first_name}, nos alegra volver a verte en la clínica."
FAREWELL_SUBJECT = "Gracias por confiar en la clínica"
FAREWELL_BODY = "Hola {first_name}, tu baja como paciente se ha completado. Te deseamos lo mejor."


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

    async def welcome_back(self, patient: PatientDto) -> None:
        await self._send(
            patient=patient,
            subject=WELCOME_BACK_SUBJECT,
            body=WELCOME_BACK_BODY.format(first_name=patient.first_name),
        )

    async def farewell(self, patient: PatientDto) -> None:
        await self._send(
            patient=patient,
            subject=FAREWELL_SUBJECT,
            body=FAREWELL_BODY.format(first_name=patient.first_name),
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
