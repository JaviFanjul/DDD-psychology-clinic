from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_command_repository import (
    AppointmentCommandRepository,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.errors import AppointmentNotFound


@dataclass(frozen=True)
class CancelAppointmentCommand(Command):
    id: AppointmentId


class CancelAppointmentCommandHandler(CommandHandler[CancelAppointmentCommand]):
    def __init__(self, repository: AppointmentCommandRepository, event_bus: EventBus) -> None:
        self._repository = repository
        self._event_bus = event_bus

    async def handle(self, command: CancelAppointmentCommand) -> None:
        appointment: Appointment | None = await self._repository.find_by_id(id=command.id)
        if appointment is None:
            raise AppointmentNotFound(id=str(command.id))
        appointment.cancel()
        await self._repository.save(appointment=appointment)
        await self._event_bus.publish(events=appointment.pull_events())
