from dataclasses import dataclass

from assistant.domain.command_bus import Command, CommandHandler
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_command_repository import PatientCommandRepository
from assistant.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class ActivatePatientCommand(Command[None]):
    id: PatientId


class ActivatePatientCommandHandler(CommandHandler[ActivatePatientCommand, None]):
    def __init__(self, repository: PatientCommandRepository) -> None:
        self._repository = repository

    async def handle(self, command: ActivatePatientCommand) -> None:
        patient: Patient | None = await self._repository.find_by_id(id=command.id)
        if patient is None:
            patient = Patient.create(id=command.id)
        else:
            patient.activate()
        await self._repository.save(patient=patient)
