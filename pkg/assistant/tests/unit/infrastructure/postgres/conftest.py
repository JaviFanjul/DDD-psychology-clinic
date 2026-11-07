from uuid import UUID

import pytest
from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_id import PatientId
from assistant.infrastructure.postgres.conversation_model import ConversationModel
from assistant.infrastructure.postgres.patient_model import PatientModel
from sqlalchemy.exc import SQLAlchemyError

PATIENT_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"
CONVERSATION_ID = "12345678-1234-4678-9234-567812345678"


class FailingSession:
    def __init__(self) -> None:
        self.rolled_back = False

    async def merge(self, instance):
        raise SQLAlchemyError("database unavailable")

    async def rollback(self):
        self.rolled_back = True

    async def get(self, entity, ident):
        raise SQLAlchemyError("database unavailable")


@pytest.fixture
def failing_session() -> FailingSession:
    return FailingSession()


@pytest.fixture
def patient() -> Patient:
    return Patient.create(id=PatientId.from_string(id=PATIENT_ID))


@pytest.fixture
def patient_model() -> PatientModel:
    return PatientModel(id=UUID(PATIENT_ID), active=True)


@pytest.fixture
def conversation() -> Conversation:
    return Conversation(
        id=ConversationId.from_string(id=CONVERSATION_ID),
        patient_id=PatientId.from_string(id=PATIENT_ID),
        messages=[
            Message(type=MessageType.PATIENT, content="Me cuesta dormir"),
            Message(
                type=MessageType.ASSISTANT,
                content="",
                tool_calls=(ToolCall(id="call-1", name="find_sessions", arguments={"limit": 1}),),
            ),
            Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1"),
            Message(type=MessageType.ASSISTANT, content="¿Desde cuándo?"),
        ],
    )


@pytest.fixture
def conversation_model() -> ConversationModel:
    return ConversationModel(
        id=UUID(CONVERSATION_ID),
        patient_id=UUID(PATIENT_ID),
        messages=[
            {
                "type": "patient",
                "content": "Me cuesta dormir",
                "tool_calls": [],
                "tool_call_id": None,
            },
            {
                "type": "assistant",
                "content": "",
                "tool_calls": [{"id": "call-1", "name": "find_sessions", "arguments": {"limit": 1}}],
                "tool_call_id": None,
            },
            {
                "type": "tool",
                "content": "Última sesión: lunes",
                "tool_calls": [],
                "tool_call_id": "call-1",
            },
            {
                "type": "assistant",
                "content": "¿Desde cuándo?",
                "tool_calls": [],
                "tool_call_id": None,
            },
        ],
    )
