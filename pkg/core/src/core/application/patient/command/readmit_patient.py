from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_id import PatientId
from core.domain.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class ReadmitPatientCommand(Command):
    id: PatientId


class ReadmitPatientCommandHandler(CommandHandler[ReadmitPatientCommand]):
    def __init__(self, repository: PatientCommandRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._event_bus = event_bus

    async def handle(self, command: ReadmitPatientCommand) -> None:
        async with self._unit_of_work:
            patient: Patient | None = await self._repository.find_by_id(id=command.id)
            if patient is None:
                raise PatientNotFound(id=str(command.id))
            patient.readmit()
            await self._repository.save(patient=patient)
            await self._unit_of_work.commit()
        await self._event_bus.publish(events=patient.pull_events())
