from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_command_repository import (
    AppointmentCommandRepository,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.errors import AppointmentNotFound, AppointmentOverlaps
from core.domain.model.appointment.psychologist_availability import PsychologistAvailability


@dataclass(frozen=True)
class RescheduleAppointmentCommand(Command):
    id: AppointmentId
    slot: AppointmentSlot


class RescheduleAppointmentCommandHandler(CommandHandler[RescheduleAppointmentCommand]):
    def __init__(
        self,
        repository: AppointmentCommandRepository,
        availability: PsychologistAvailability,
        event_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._availability = availability
        self._event_bus = event_bus

    async def handle(self, command: RescheduleAppointmentCommand) -> None:
        appointment: Appointment | None = await self._repository.find_by_id(id=command.id)
        if appointment is None:
            raise AppointmentNotFound(id=str(command.id))
        appointment.reschedule(slot=command.slot)
        if not await self._availability.is_available(
            psychologist_id=appointment.psychologist_id, slot=command.slot, excluding=command.id
        ):
            raise AppointmentOverlaps(psychologist_id=str(appointment.psychologist_id))
        await self._repository.save(appointment=appointment)
        await self._event_bus.publish(events=appointment.pull_events())
