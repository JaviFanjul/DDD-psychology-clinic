from typing import Any

import pytest
from assistant.domain.command_bus import Command, CommandBus
from assistant.domain.model.conversation.conversation_query_repository import (
    ConversationDto,
    MessageDto,
)
from assistant.domain.model.conversation.message import Message, MessageType
from assistant.domain.query_bus import Query, QueryBus
from assistant.entrypoint.conversation.http.conversation_controller import ConversationController

CONVERSATION_ID = "12345678-1234-4678-9234-567812345678"
PATIENT_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


class SpyCommandBus(CommandBus):
    def __init__(self, result: Any) -> None:
        self._result = result
        self.handled: list[Command[Any]] = []

    async def handle[TResult](self, command: Command[TResult]) -> TResult:
        self.handled.append(command)
        result: TResult = self._result
        return result


class SpyQueryBus(QueryBus):
    def __init__(self, result: ConversationDto) -> None:
        self._result = result
        self.handled: list[Query[Any]] = []

    async def handle[TResult](self, query: Query[TResult]) -> TResult:
        self.handled.append(query)
        result: TResult = self._result
        return result


@pytest.fixture
def conversation_id() -> str:
    return CONVERSATION_ID


@pytest.fixture
def patient_id() -> str:
    return PATIENT_ID


@pytest.fixture
def reply() -> Message:
    return Message(type=MessageType.ASSISTANT, content="¿Desde cuándo te pasa?")


@pytest.fixture
def conversation_dto() -> ConversationDto:
    return ConversationDto(
        id=CONVERSATION_ID,
        patient_id=PATIENT_ID,
        messages=[MessageDto(type="patient", content="Me cuesta dormir")],
    )


@pytest.fixture
def command_bus(reply: Message) -> SpyCommandBus:
    return SpyCommandBus(result=reply)


@pytest.fixture
def query_bus(conversation_dto: ConversationDto) -> SpyQueryBus:
    return SpyQueryBus(result=conversation_dto)


@pytest.fixture
def controller(command_bus: SpyCommandBus, query_bus: SpyQueryBus) -> ConversationController:
    return ConversationController(command_bus=command_bus, query_bus=query_bus)
