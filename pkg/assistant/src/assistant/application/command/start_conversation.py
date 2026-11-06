from dataclasses import dataclass

from assistant.domain.command_bus import Command, CommandHandler
from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_command_repository import (
    ConversationCommandRepository,
)
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.patient.errors import PatientNotActive, PatientNotFound
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_command_repository import PatientCommandRepository
from assistant.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class StartConversationCommand(Command[None]):
    id: ConversationId
    patient_id: PatientId


class StartConversationCommandHandler(CommandHandler[StartConversationCommand, None]):
    def __init__(
        self,
        conversations: ConversationCommandRepository,
        patients: PatientCommandRepository,
    ) -> None:
        self._conversations = conversations
        self._patients = patients

    async def handle(self, command: StartConversationCommand) -> None:
        patient: Patient | None = await self._patients.find_by_id(id=command.patient_id)
        if patient is None:
            raise PatientNotFound(id=str(command.patient_id))
        if not patient.is_active:
            raise PatientNotActive(id=str(command.patient_id))
        conversation: Conversation = Conversation.start(
            id=command.id, patient_id=command.patient_id
        )
        await self._conversations.save(conversation=conversation)
