from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class DischargePatientCommand(Command):
    id: PatientId


class DischargePatientCommandHandler(CommandHandler[DischargePatientCommand]):
    def __init__(self, repository: PatientCommandRepository, event_bus: EventBus) -> None:
        self._repository = repository
        self._event_bus = event_bus

    async def handle(self, command: DischargePatientCommand) -> None:
        patient: Patient | None = await self._repository.find_by_id(id=command.id)
        if patient is None:
            raise PatientNotFound(id=str(command.id))
        patient.discharge()
        await self._repository.save(patient=patient)
        await self._event_bus.publish(events=patient.pull_events())
