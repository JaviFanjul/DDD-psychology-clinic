from datetime import datetime
from http import HTTPStatus

from core.application.command.cancel_appointment import CancelAppointmentCommand
from core.application.command.change_appointment_modality import (
    ChangeAppointmentModalityCommand,
)
from core.application.command.complete_appointment import CompleteAppointmentCommand
from core.application.command.reschedule_appointment import RescheduleAppointmentCommand
from core.application.command.schedule_appointment import ScheduleAppointmentCommand
from core.application.query.get_appointment import GetAppointmentQuery
from core.domain.command_bus import CommandBus
from core.domain.domain_error import DomainError
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.errors import (
    AppointmentAlreadyCancelled,
    AppointmentAlreadyCompleted,
    AppointmentNotFound,
    AppointmentNotLoaded,
    AppointmentNotSaved,
    AppointmentOverlaps,
    InvalidAppointmentId,
    InvalidAppointmentModality,
    InvalidAppointmentSlot,
)
from core.domain.model.patient.errors import (
    InvalidPatientId,
    PatientNotActive,
    PatientNotFound,
    PatientNotLoaded,
)
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.errors import (
    InvalidPsychologistId,
    PsychologistNotFound,
    PsychologistNotLoaded,
)
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.query_bus import QueryBus

STATUS_BY_ERROR: dict[type[DomainError], HTTPStatus] = {
    InvalidAppointmentId: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidAppointmentSlot: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidAppointmentModality: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPatientId: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPsychologistId: HTTPStatus.UNPROCESSABLE_CONTENT,
    AppointmentNotFound: HTTPStatus.NOT_FOUND,
    PatientNotFound: HTTPStatus.NOT_FOUND,
    PsychologistNotFound: HTTPStatus.NOT_FOUND,
    PatientNotActive: HTTPStatus.CONFLICT,
    AppointmentOverlaps: HTTPStatus.CONFLICT,
    AppointmentAlreadyCancelled: HTTPStatus.CONFLICT,
    AppointmentAlreadyCompleted: HTTPStatus.CONFLICT,
    AppointmentNotSaved: HTTPStatus.INTERNAL_SERVER_ERROR,
    AppointmentNotLoaded: HTTPStatus.INTERNAL_SERVER_ERROR,
    PatientNotLoaded: HTTPStatus.INTERNAL_SERVER_ERROR,
    PsychologistNotLoaded: HTTPStatus.INTERNAL_SERVER_ERROR,
}


class AppointmentController:
    def __init__(self, command_bus: CommandBus, query_bus: QueryBus) -> None:
        self._command_bus = command_bus
        self._query_bus = query_bus

    async def schedule(
        self,
        patient_id: str,
        psychologist_id: str,
        starts_at: datetime,
        duration_minutes: int,
        modality: str,
    ) -> str:
        appointment_id: AppointmentId = AppointmentId.generate()
        appointment_patient_id: PatientId = PatientId.from_string(id=patient_id)
        appointment_psychologist_id: PsychologistId = PsychologistId.from_string(id=psychologist_id)
        appointment_slot: AppointmentSlot = AppointmentSlot(
            starts_at=starts_at, duration_minutes=duration_minutes
        )
        appointment_modality: AppointmentModality = AppointmentModality.from_string(value=modality)
        await self._command_bus.handle(
            command=ScheduleAppointmentCommand(
                id=appointment_id,
                patient_id=appointment_patient_id,
                psychologist_id=appointment_psychologist_id,
                slot=appointment_slot,
                modality=appointment_modality,
            )
        )
        return str(appointment_id)

    async def get(self, id: str) -> AppointmentDto:
        appointment_id: AppointmentId = AppointmentId.from_string(id=id)
        return await self._query_bus.handle(query=GetAppointmentQuery(id=appointment_id))

    async def reschedule(self, id: str, starts_at: datetime, duration_minutes: int) -> None:
        appointment_id: AppointmentId = AppointmentId.from_string(id=id)
        appointment_slot: AppointmentSlot = AppointmentSlot(
            starts_at=starts_at, duration_minutes=duration_minutes
        )
        await self._command_bus.handle(
            command=RescheduleAppointmentCommand(id=appointment_id, slot=appointment_slot)
        )

    async def change_modality(self, id: str, modality: str) -> None:
        appointment_id: AppointmentId = AppointmentId.from_string(id=id)
        appointment_modality: AppointmentModality = AppointmentModality.from_string(value=modality)
        await self._command_bus.handle(
            command=ChangeAppointmentModalityCommand(
                id=appointment_id, modality=appointment_modality
            )
        )

    async def cancel(self, id: str) -> None:
        appointment_id: AppointmentId = AppointmentId.from_string(id=id)
        await self._command_bus.handle(command=CancelAppointmentCommand(id=appointment_id))

    async def complete(self, id: str) -> None:
        appointment_id: AppointmentId = AppointmentId.from_string(id=id)
        await self._command_bus.handle(command=CompleteAppointmentCommand(id=appointment_id))
