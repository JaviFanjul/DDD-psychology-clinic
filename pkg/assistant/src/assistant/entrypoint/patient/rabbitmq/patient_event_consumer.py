import json

from aio_pika.abc import AbstractIncomingMessage
from assistant.application.command.activate_patient import ActivatePatientCommand
from assistant.application.command.deactivate_patient import DeactivatePatientCommand
from assistant.domain.command_bus import CommandBus
from assistant.domain.model.patient.patient_id import PatientId

CORE_EXCHANGE = "core"
PATIENT_EVENTS_QUEUE = "assistant.patients"
COMMAND_BY_ROUTING_KEY: dict[str, type[ActivatePatientCommand | DeactivatePatientCommand]] = {
    "patient.created": ActivatePatientCommand,
    "patient.readmitted": ActivatePatientCommand,
    "patient.discharged": DeactivatePatientCommand,
}


class PatientEventConsumer:
    def __init__(self, command_bus: CommandBus) -> None:
        self._command_bus = command_bus

    async def consume(self, message: AbstractIncomingMessage) -> None:
        async with message.process(requeue=True):
            patient_id: PatientId = PatientId.from_string(id=json.loads(message.body)["patient_id"])
            command_type = COMMAND_BY_ROUTING_KEY[str(message.routing_key)]
            await self._command_bus.handle(command=command_type(id=patient_id))
