from email.message import EmailMessage
from zoneinfo import ZoneInfo

import aiosmtplib
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.patient.errors import PatientNotNotified
from core.domain.model.patient.patient_notifier import PatientNotifier
from core.domain.model.patient.patient_query_repository import PatientDto

WELCOME_SUBJECT = "Te damos la bienvenida a la clínica"
WELCOME_BODY = "Hola {first_name}, tu alta como paciente se ha completado."
WELCOME_BACK_SUBJECT = "Te damos la bienvenida de nuevo a la clínica"
WELCOME_BACK_BODY = "Hola {first_name}, nos alegra volver a verte en la clínica."
FAREWELL_SUBJECT = "Gracias por confiar en la clínica"
FAREWELL_BODY = "Hola {first_name}, tu baja como paciente se ha completado. Te deseamos lo mejor."
APPOINTMENT_SCHEDULED_SUBJECT = "Tu consulta ha quedado agendada"
APPOINTMENT_SCHEDULED_BODY = (
    "Hola {first_name}, tu consulta {modality} del {date} a las {time} "
    "({duration} minutos) ha quedado agendada."
)
APPOINTMENT_RESCHEDULED_SUBJECT = "Tu consulta ha cambiado de fecha"
APPOINTMENT_RESCHEDULED_BODY = (
    "Hola {first_name}, tu consulta {modality} ahora es el {date} a las {time} "
    "({duration} minutos)."
)
APPOINTMENT_MODALITY_CHANGED_SUBJECT = "Tu consulta ha cambiado de modalidad"
APPOINTMENT_MODALITY_CHANGED_BODY = (
    "Hola {first_name}, tu consulta del {date} a las {time} ahora es {modality}."
)
APPOINTMENT_CANCELLED_SUBJECT = "Tu consulta ha sido cancelada"
APPOINTMENT_CANCELLED_BODY = (
    "Hola {first_name}, tu consulta del {date} a las {time} ha sido cancelada."
)
FEEDBACK_SUBJECT = "¿Qué tal fue tu consulta?"
FEEDBACK_BODY = (
    "Hola {first_name}, gracias por venir a tu consulta del {date}. "
    "Nos encantaría saber qué tal fue: responde a este correo y cuéntanos tu opinión."
)
CLINIC_TIMEZONE = ZoneInfo("Europe/Madrid")
MODALITY_NAMES: dict[AppointmentModality, str] = {
    AppointmentModality.IN_PERSON: "presencial",
    AppointmentModality.ONLINE: "online",
}


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

    async def appointment_scheduled(self, patient: PatientDto, appointment: AppointmentDto) -> None:
        await self._send_about_appointment(
            patient=patient,
            appointment=appointment,
            subject=APPOINTMENT_SCHEDULED_SUBJECT,
            body=APPOINTMENT_SCHEDULED_BODY,
        )

    async def appointment_rescheduled(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None:
        await self._send_about_appointment(
            patient=patient,
            appointment=appointment,
            subject=APPOINTMENT_RESCHEDULED_SUBJECT,
            body=APPOINTMENT_RESCHEDULED_BODY,
        )

    async def appointment_modality_changed(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None:
        await self._send_about_appointment(
            patient=patient,
            appointment=appointment,
            subject=APPOINTMENT_MODALITY_CHANGED_SUBJECT,
            body=APPOINTMENT_MODALITY_CHANGED_BODY,
        )

    async def appointment_cancelled(self, patient: PatientDto, appointment: AppointmentDto) -> None:
        await self._send_about_appointment(
            patient=patient,
            appointment=appointment,
            subject=APPOINTMENT_CANCELLED_SUBJECT,
            body=APPOINTMENT_CANCELLED_BODY,
        )

    async def request_feedback(self, patient: PatientDto, appointment: AppointmentDto) -> None:
        await self._send_about_appointment(
            patient=patient, appointment=appointment, subject=FEEDBACK_SUBJECT, body=FEEDBACK_BODY
        )

    async def _send_about_appointment(
        self, patient: PatientDto, appointment: AppointmentDto, subject: str, body: str
    ) -> None:
        await self._send(
            patient=patient,
            subject=subject,
            body=body.format(
                first_name=patient.first_name, **self._appointment_details(appointment=appointment)
            ),
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
