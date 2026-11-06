from dataclasses import dataclass

from assistant.domain.command_bus import Command, CommandHandler
from assistant.domain.model.patient.errors import PatientNotFound
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_command_repository import PatientCommandRepository
from assistant.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class DeactivatePatientCommand(Command[None]):
    id: PatientId


class DeactivatePatientCommandHandler(CommandHandler[DeactivatePatientCommand, None]):
    def __init__(self, repository: PatientCommandRepository) -> None:
        self._repository = repository

    async def handle(self, command: DeactivatePatientCommand) -> None:
        patient: Patient | None = await self._repository.find_by_id(id=command.id)
        if patient is None:
            raise PatientNotFound(id=str(command.id))
        patient.deactivate()
        await self._repository.save(patient=patient)
