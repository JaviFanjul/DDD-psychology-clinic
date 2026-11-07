from typing import Any

from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.conversation_query_repository import (
    ConversationDto,
    MessageDto,
)
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from assistant.domain.model.patient.patient_id import PatientId
from assistant.infrastructure.postgres.conversation_model import ConversationModel


class ConversationMapper:
    @staticmethod
    def to_model(conversation: Conversation) -> ConversationModel:
        return ConversationModel(
            id=conversation.id.id,
            patient_id=conversation.patient_id.id,
            messages=[ConversationMapper._message_to_json(message=message) for message in conversation.messages],
        )

    @staticmethod
    def to_entity(model: ConversationModel) -> Conversation:
        return Conversation(
            id=ConversationId(id=model.id),
            patient_id=PatientId(id=model.patient_id),
            messages=[ConversationMapper._message_from_json(message=message) for message in model.messages],
        )

    @staticmethod
    def to_dto(model: ConversationModel) -> ConversationDto:
        return ConversationDto(
            id=str(model.id),
            patient_id=str(model.patient_id),
            messages=[
                MessageDto(type=message["type"], content=message["content"])
                for message in model.messages
                if message["type"] == MessageType.PATIENT
                or (message["type"] == MessageType.ASSISTANT and message["content"].strip())
            ],
        )

    @staticmethod
    def _message_to_json(message: Message) -> dict[str, Any]:
        return {
            "type": message.type.value,
            "content": message.content,
            "tool_calls": [
                {"id": tool_call.id, "name": tool_call.name, "arguments": tool_call.arguments}
                for tool_call in message.tool_calls
            ],
            "tool_call_id": message.tool_call_id,
        }

    @staticmethod
    def _message_from_json(message: dict[str, Any]) -> Message:
        return Message(
            type=MessageType(message["type"]),
            content=message["content"],
            tool_calls=tuple(
                ToolCall(id=tool_call["id"], name=tool_call["name"], arguments=tool_call["arguments"])
                for tool_call in message["tool_calls"]
            ),
            tool_call_id=message["tool_call_id"],
        )
