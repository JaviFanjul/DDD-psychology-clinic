from core.domain.domain_event import DomainEvent
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import (
    AppointmentAlreadyCancelled,
    AppointmentAlreadyCompleted,
)
from core.domain.model.appointment.events import (
    AppointmentCancelled,
    AppointmentCompleted,
    AppointmentModalityChanged,
    AppointmentRescheduled,
    AppointmentScheduled,
)
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.psychologist_id import PsychologistId


class Appointment:
    def __init__(
        self,
        id: AppointmentId,
        patient_id: PatientId,
        psychologist_id: PsychologistId,
        slot: AppointmentSlot,
        modality: AppointmentModality,
        status: AppointmentStatus,
    ) -> None:
        self._id = id
        self._patient_id = patient_id
        self._psychologist_id = psychologist_id
        self._slot = slot
        self._modality = modality
        self._status = status
        self._events: list[DomainEvent] = []

    @property
    def id(self) -> AppointmentId:
        return self._id

    @property
    def patient_id(self) -> PatientId:
        return self._patient_id

    @property
    def psychologist_id(self) -> PsychologistId:
        return self._psychologist_id

    @property
    def slot(self) -> AppointmentSlot:
        return self._slot

    @property
    def modality(self) -> AppointmentModality:
        return self._modality

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    @classmethod
    def schedule(
        cls,
        id: AppointmentId,
        patient_id: PatientId,
        psychologist_id: PsychologistId,
        slot: AppointmentSlot,
        modality: AppointmentModality,
    ) -> Appointment:
        appointment: Appointment = cls(
            id=id,
            patient_id=patient_id,
            psychologist_id=psychologist_id,
            slot=slot,
            modality=modality,
            status=AppointmentStatus.PENDING,
        )
        appointment._events.append(AppointmentScheduled(appointment_id=id))
        return appointment

    def reschedule(self, slot: AppointmentSlot) -> None:
        self._ensure_pending()
        if slot == self._slot:
            return
        self._slot = slot
        self._events.append(AppointmentRescheduled(appointment_id=self._id))

    def change_modality(self, modality: AppointmentModality) -> None:
        self._ensure_pending()
        if modality is self._modality:
            return
        self._modality = modality
        self._events.append(AppointmentModalityChanged(appointment_id=self._id))

    def cancel(self) -> None:
        self._ensure_pending()
        self._status = AppointmentStatus.CANCELLED
        self._events.append(AppointmentCancelled(appointment_id=self._id))

    def complete(self) -> None:
        self._ensure_pending()
        self._status = AppointmentStatus.COMPLETED
        self._events.append(AppointmentCompleted(appointment_id=self._id))

    def _ensure_pending(self) -> None:
        if self._status is AppointmentStatus.CANCELLED:
            raise AppointmentAlreadyCancelled(id=str(self._id))
        if self._status is AppointmentStatus.COMPLETED:
            raise AppointmentAlreadyCompleted(id=str(self._id))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Appointment) and other._id == self._id

    def __hash__(self) -> int:
        return hash(self._id)

    def pull_events(self) -> list[DomainEvent]:
        events: list[DomainEvent] = self._events
        self._events = []
        return events
