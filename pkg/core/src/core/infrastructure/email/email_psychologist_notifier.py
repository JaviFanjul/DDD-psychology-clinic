from email.message import EmailMessage
from zoneinfo import ZoneInfo

import aiosmtplib
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.psychologist.errors import PsychologistNotNotified
from core.domain.model.psychologist.psychologist_notifier import PsychologistNotifier
from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto

APPOINTMENT_SCHEDULED_SUBJECT = "Tienes una nueva consulta"
APPOINTMENT_SCHEDULED_BODY = (
    "Hola {first_name}, tienes una nueva consulta {modality} el {date} a las {time} "
    "({duration} minutos)."
)
APPOINTMENT_RESCHEDULED_SUBJECT = "Una consulta ha cambiado de fecha"
APPOINTMENT_RESCHEDULED_BODY = (
    "Hola {first_name}, tu consulta {modality} ahora es el {date} a las {time} "
    "({duration} minutos)."
)
APPOINTMENT_MODALITY_CHANGED_SUBJECT = "Una consulta ha cambiado de modalidad"
APPOINTMENT_MODALITY_CHANGED_BODY = (
    "Hola {first_name}, tu consulta del {date} a las {time} ahora es {modality}."
)
APPOINTMENT_CANCELLED_SUBJECT = "Una consulta ha sido cancelada"
APPOINTMENT_CANCELLED_BODY = (
    "Hola {first_name}, tu consulta del {date} a las {time} ha sido cancelada."
)
CLINIC_TIMEZONE = ZoneInfo("Europe/Madrid")
MODALITY_NAMES: dict[AppointmentModality, str] = {
    AppointmentModality.IN_PERSON: "presencial",
    AppointmentModality.ONLINE: "online",
}


class EmailPsychologistNotifier(PsychologistNotifier):
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

    async def appointment_scheduled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        await self._send(
            psychologist=psychologist,
            appointment=appointment,
            subject=APPOINTMENT_SCHEDULED_SUBJECT,
            body=APPOINTMENT_SCHEDULED_BODY,
        )

    async def appointment_rescheduled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        await self._send(
            psychologist=psychologist,
            appointment=appointment,
            subject=APPOINTMENT_RESCHEDULED_SUBJECT,
            body=APPOINTMENT_RESCHEDULED_BODY,
        )

    async def appointment_modality_changed(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        await self._send(
            psychologist=psychologist,
            appointment=appointment,
            subject=APPOINTMENT_MODALITY_CHANGED_SUBJECT,
            body=APPOINTMENT_MODALITY_CHANGED_BODY,
        )

    async def appointment_cancelled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None:
        await self._send(
            psychologist=psychologist,
            appointment=appointment,
            subject=APPOINTMENT_CANCELLED_SUBJECT,
            body=APPOINTMENT_CANCELLED_BODY,
        )

    async def _send(
        self, psychologist: PsychologistDto, appointment: AppointmentDto, subject: str, body: str
    ) -> None:
        message = EmailMessage()
        message["From"] = self._sender
        message["To"] = psychologist.email
        message["Subject"] = subject
        message.set_content(
            body.format(
                first_name=psychologist.first_name,
                **self._appointment_details(appointment=appointment),
            )
        )
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
            raise PsychologistNotNotified(id=psychologist.id) from error

    @staticmethod
    def _appointment_details(appointment: AppointmentDto) -> dict[str, str]:
        starts_at = appointment.starts_at.astimezone(CLINIC_TIMEZONE)
        modality: AppointmentModality = AppointmentModality(appointment.modality)
        return {
            "date": starts_at.strftime("%d/%m/%Y"),
            "time": starts_at.strftime("%H:%M"),
            "duration": str(appointment.duration_minutes),
            "modality": MODALITY_NAMES[modality],
        }
