from core.domain.event_bus import EventHandler
from core.domain.model.appointment.appointment_query_repository import (
    AppointmentDto,
    AppointmentQueryRepository,
)
from core.domain.model.appointment.errors import AppointmentNotFound
from core.domain.model.appointment.events import AppointmentRescheduled
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_notifier import PatientNotifier
from core.domain.model.patient.patient_query_repository import PatientDto, PatientQueryRepository


class NotifyPatientOnAppointmentRescheduled(EventHandler[AppointmentRescheduled]):
    def __init__(
        self,
        appointments: AppointmentQueryRepository,
        patients: PatientQueryRepository,
        notifier: PatientNotifier,
    ) -> None:
        self._appointments = appointments
        self._patients = patients
        self._notifier = notifier

    async def handle(self, event: AppointmentRescheduled) -> None:
        appointment: AppointmentDto | None = await self._appointments.find_by_id(
            id=event.appointment_id
        )
        if appointment is None:
            raise AppointmentNotFound(id=str(event.appointment_id))
        patient_id: PatientId = PatientId.from_string(id=appointment.patient_id)
        patient: PatientDto | None = await self._patients.find_by_id(id=patient_id)
        if patient is None:
            raise PatientNotFound(id=appointment.patient_id)
        await self._notifier.appointment_rescheduled(patient=patient, appointment=appointment)
