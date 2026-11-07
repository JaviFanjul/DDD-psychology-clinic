from dataclasses import dataclass

from core.domain.command_bus import Command, CommandHandler
from core.domain.event_bus import EventBus
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone
from core.domain.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class CreatePatientCommand(Command):
    id: PatientId
    email: PatientEmail
    name: PatientName
    phone: PatientPhone
    address: PatientAddress


class CreatePatientCommandHandler(CommandHandler[CreatePatientCommand]):
    def __init__(self, repository: PatientCommandRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._event_bus = event_bus

    async def handle(self, command: CreatePatientCommand) -> None:
        async with self._unit_of_work:
            patient: Patient = Patient.create(
                id=command.id,
                email=command.email,
                name=command.name,
                phone=command.phone,
                address=command.address,
            )
            await self._repository.save(patient=patient)
            await self._unit_of_work.commit()
        await self._event_bus.publish(events=patient.pull_events())
