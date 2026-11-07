from http import HTTPStatus

from assistant.application.command.start_conversation import StartConversationCommand
from assistant.application.command.talk_to_assistant import TalkToAssistantCommand
from assistant.application.query.get_conversation import GetConversationQuery
from assistant.domain.command_bus import CommandBus
from assistant.domain.domain_error import DomainError
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.conversation_query_repository import ConversationDto
from assistant.domain.model.conversation.errors import (
    AssistantNotAnswered,
    ConversationNotFound,
    ConversationNotLoaded,
    ConversationNotOwned,
    ConversationNotSaved,
    InvalidConversationId,
)
from assistant.domain.model.conversation.message import Message
from assistant.domain.model.patient.errors import (
    InvalidPatientId,
    PatientNotActive,
    PatientNotFound,
    PatientNotLoaded,
)
from assistant.domain.model.patient.patient_id import PatientId
from assistant.domain.query_bus import QueryBus

STATUS_BY_ERROR: dict[type[DomainError], HTTPStatus] = {
    InvalidConversationId: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPatientId: HTTPStatus.UNPROCESSABLE_CONTENT,
    ConversationNotFound: HTTPStatus.NOT_FOUND,
    PatientNotFound: HTTPStatus.NOT_FOUND,
    ConversationNotOwned: HTTPStatus.FORBIDDEN,
    PatientNotActive: HTTPStatus.CONFLICT,
    ConversationNotSaved: HTTPStatus.INTERNAL_SERVER_ERROR,
    ConversationNotLoaded: HTTPStatus.INTERNAL_SERVER_ERROR,
    PatientNotLoaded: HTTPStatus.INTERNAL_SERVER_ERROR,
    AssistantNotAnswered: HTTPStatus.BAD_GATEWAY,
}


class ConversationController:
    def __init__(self, command_bus: CommandBus, query_bus: QueryBus) -> None:
        self._command_bus = command_bus
        self._query_bus = query_bus

    async def start(self, patient_id: str) -> str:
        conversation_id: ConversationId = ConversationId.generate()
        owner_id: PatientId = PatientId.from_string(id=patient_id)
        await self._command_bus.handle(command=StartConversationCommand(id=conversation_id, patient_id=owner_id))
        return str(conversation_id)

    async def talk(self, id: str, patient_id: str, content: str) -> str:
        conversation_id: ConversationId = ConversationId.from_string(id=id)
        owner_id: PatientId = PatientId.from_string(id=patient_id)
        reply: Message = await self._command_bus.handle(
            command=TalkToAssistantCommand(conversation_id=conversation_id, patient_id=owner_id, content=content)
        )
        return reply.content

    async def get(self, id: str) -> ConversationDto:
        conversation_id: ConversationId = ConversationId.from_string(id=id)
        return await self._query_bus.handle(query=GetConversationQuery(id=conversation_id))
