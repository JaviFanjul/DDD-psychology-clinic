from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class RegisterPatientCommand(Command):
    id: PatientId
    email: PatientEmail


class RegisterPatientCommandHandler(CommandHandler[RegisterPatientCommand]):
    def __init__(self, repository: PatientCommandRepository, event_bus: EventBus) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: RegisterPatientCommand) -> None:
        patient = Patient.register(command.id, command.email)
        self._repository.save(patient)
        self._event_bus.publish(patient.pull_events())
