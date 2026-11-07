from dataclasses import dataclass

from assistant.domain.command_bus import Command, CommandHandler
from assistant.domain.model.conversation.assistant import Assistant
from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_command_repository import (
    ConversationCommandRepository,
)
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import ConversationNotFound
from assistant.domain.model.conversation.message import Message
from assistant.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class TalkToAssistantCommand(Command[Message]):
    conversation_id: ConversationId
    patient_id: PatientId
    content: str


class TalkToAssistantCommandHandler(CommandHandler[TalkToAssistantCommand, Message]):
    def __init__(self, conversations: ConversationCommandRepository, assistant: Assistant) -> None:
        self._conversations = conversations
        self._assistant = assistant

    async def handle(self, command: TalkToAssistantCommand) -> Message:
        conversation: Conversation | None = await self._conversations.find_by_id(id=command.conversation_id)
        if conversation is None:
            raise ConversationNotFound(id=str(command.conversation_id))
        conversation.patient_writes(patient_id=command.patient_id, content=command.content)
        replies: list[Message] = await self._assistant.ask(messages=conversation.messages)
        conversation.assistant_replies(messages=replies)
        await self._conversations.save(conversation=conversation)
        return replies[-1]
