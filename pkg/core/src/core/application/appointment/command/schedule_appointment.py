from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_command_repository import (
    AppointmentCommandRepository,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.errors import AppointmentOverlaps
from core.domain.model.appointment.psychologist_availability import PsychologistAvailability
from core.domain.model.patient.errors import PatientNotActive, PatientNotFound
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_query_repository import PatientDto, PatientQueryRepository
from core.domain.model.patient.patient_status import PatientStatus
from core.domain.model.psychologist.errors import PsychologistNotFound
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_query_repository import (
    PsychologistDto,
    PsychologistQueryRepository,
)


@dataclass(frozen=True)
class ScheduleAppointmentCommand(Command):
    id: AppointmentId
    patient_id: PatientId
    psychologist_id: PsychologistId
    slot: AppointmentSlot
    modality: AppointmentModality


class ScheduleAppointmentCommandHandler(CommandHandler[ScheduleAppointmentCommand]):
    def __init__(
        self,
        repository: AppointmentCommandRepository,
        availability: PsychologistAvailability,
        patients: PatientQueryRepository,
        psychologists: PsychologistQueryRepository,
        event_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._availability = availability
        self._patients = patients
        self._psychologists = psychologists
        self._event_bus = event_bus

    async def handle(self, command: ScheduleAppointmentCommand) -> None:
        patient: PatientDto | None = await self._patients.find_by_id(id=command.patient_id)
        if patient is None:
            raise PatientNotFound(id=str(command.patient_id))
        if patient.status != PatientStatus.ACTIVE:
            raise PatientNotActive(id=str(command.patient_id))
        psychologist: PsychologistDto | None = await self._psychologists.find_by_id(id=command.psychologist_id)
        if psychologist is None:
            raise PsychologistNotFound(id=str(command.psychologist_id))
        if not await self._availability.is_available(
            psychologist_id=command.psychologist_id, slot=command.slot, excluding=command.id
        ):
            raise AppointmentOverlaps(psychologist_id=str(command.psychologist_id))
        appointment: Appointment = Appointment.schedule(
            id=command.id,
            patient_id=command.patient_id,
            psychologist_id=command.psychologist_id,
            slot=command.slot,
            modality=command.modality,
        )
        await self._repository.save(appointment=appointment)
        await self._event_bus.publish(events=appointment.pull_events())
