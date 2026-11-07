from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_command_repository import (
    AppointmentCommandRepository,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.errors import AppointmentNotFound
from core.domain.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class ChangeAppointmentModalityCommand(Command):
    id: AppointmentId
    modality: AppointmentModality


class ChangeAppointmentModalityCommandHandler(CommandHandler[ChangeAppointmentModalityCommand]):
    def __init__(self, repository: AppointmentCommandRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._event_bus = event_bus

    async def handle(self, command: ChangeAppointmentModalityCommand) -> None:
        async with self._unit_of_work:
            appointment: Appointment | None = await self._repository.find_by_id(id=command.id)
            if appointment is None:
                raise AppointmentNotFound(id=str(command.id))
            appointment.change_modality(modality=command.modality)
            await self._repository.save(appointment=appointment)
            await self._unit_of_work.commit()
        await self._event_bus.publish(events=appointment.pull_events())
