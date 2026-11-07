from datetime import UTC

from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.infrastructure.postgres.appointment_model import AppointmentModel


class AppointmentMapper:
    @staticmethod
    def to_model(appointment: Appointment) -> AppointmentModel:
        return AppointmentModel(
            id=appointment.id.id,
            patient_id=appointment.patient_id.id,
            psychologist_id=appointment.psychologist_id.id,
            starts_at=appointment.slot.starts_at,
            duration_minutes=appointment.slot.duration_minutes,
            modality=appointment.modality.value,
            status=appointment.status.value,
        )

    @staticmethod
    def to_entity(model: AppointmentModel) -> Appointment:
        return Appointment(
            id=AppointmentId(id=model.id),
            patient_id=PatientId(id=model.patient_id),
            psychologist_id=PsychologistId(id=model.psychologist_id),
            slot=AppointmentSlot(
                starts_at=model.starts_at, duration_minutes=model.duration_minutes
            ),
            modality=AppointmentModality(model.modality),
            status=AppointmentStatus(model.status),
        )

    @staticmethod
    def to_dto(model: AppointmentModel) -> AppointmentDto:
        return AppointmentDto(
            id=str(model.id),
            patient_id=str(model.patient_id),
            psychologist_id=str(model.psychologist_id),
            starts_at=model.starts_at.astimezone(UTC),
            duration_minutes=model.duration_minutes,
            modality=model.modality,
            status=model.status,
        )
