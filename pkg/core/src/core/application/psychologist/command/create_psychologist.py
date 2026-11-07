from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_command_repository import (
    PsychologistCommandRepository,
)
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone
from core.domain.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class CreatePsychologistCommand(Command):
    id: PsychologistId
    email: PsychologistEmail
    name: PsychologistName
    phone: PsychologistPhone
    license_number: PsychologistLicenseNumber


class CreatePsychologistCommandHandler(CommandHandler[CreatePsychologistCommand]):
    def __init__(
        self, repository: PsychologistCommandRepository, unit_of_work: UnitOfWork, event_bus: EventBus
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._event_bus = event_bus

    async def handle(self, command: CreatePsychologistCommand) -> None:
        async with self._unit_of_work:
            psychologist: Psychologist = Psychologist.create(
                id=command.id,
                email=command.email,
                name=command.name,
                phone=command.phone,
                license_number=command.license_number,
            )
            await self._repository.save(psychologist=psychologist)
            await self._unit_of_work.commit()
        await self._event_bus.publish(events=psychologist.pull_events())
