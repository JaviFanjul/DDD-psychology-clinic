import pytest
from assistant.application.command.activate_patient import ActivatePatientCommandHandler
from assistant.application.command.deactivate_patient import DeactivatePatientCommandHandler
from assistant.application.command.start_conversation import StartConversationCommandHandler
from assistant.application.command.talk_to_assistant import TalkToAssistantCommandHandler
from assistant.domain.model.conversation.assistant import Assistant
from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_command_repository import (
    ConversationCommandRepository,
)
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_command_repository import PatientCommandRepository
from assistant.domain.model.patient.patient_id import PatientId


class SpyPatientCommandRepository(PatientCommandRepository):
    def __init__(self, patients: list[Patient]) -> None:
        self._patients = {patient.id: patient for patient in patients}
        self.saved: list[Patient] = []

    async def save(self, patient: Patient) -> None:
        self.saved.append(patient)

    async def find_by_id(self, id: PatientId) -> Patient | None:
        return self._patients.get(id)


class SpyConversationCommandRepository(ConversationCommandRepository):
    def __init__(self, conversations: list[Conversation]) -> None:
        self._conversations = {conversation.id: conversation for conversation in conversations}
        self.saved: list[Conversation] = []

    async def save(self, conversation: Conversation) -> None:
        self.saved.append(conversation)

    async def find_by_id(self, id: ConversationId) -> Conversation | None:
        return self._conversations.get(id)


class SpyAssistant(Assistant):
    def __init__(self, replies: list[Message]) -> None:
        self._replies = replies
        self.asked: list[list[Message]] = []

    async def ask(self, messages: list[Message]) -> list[Message]:
        self.asked.append(messages)
        return self._replies


@pytest.fixture
def active_patient() -> Patient:
    return Patient(id=PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7"), active=True)


@pytest.fixture
def inactive_patient() -> Patient:
    return Patient(id=PatientId.from_string(id="12345678-1234-4678-9234-567812345678"), active=False)


@pytest.fixture
def unknown_patient_id() -> PatientId:
    return PatientId.from_string(id="0b7e9a1c-3f2d-4c5e-8a6b-9d1e2f3a4b5c")


@pytest.fixture
def repository(active_patient: Patient, inactive_patient: Patient) -> SpyPatientCommandRepository:
    return SpyPatientCommandRepository(patients=[active_patient, inactive_patient])


@pytest.fixture
def activate_handler(repository: SpyPatientCommandRepository) -> ActivatePatientCommandHandler:
    return ActivatePatientCommandHandler(repository=repository)


@pytest.fixture
def deactivate_handler(
    repository: SpyPatientCommandRepository,
) -> DeactivatePatientCommandHandler:
    return DeactivatePatientCommandHandler(repository=repository)


@pytest.fixture
def earlier_messages() -> list[Message]:
    return [
        Message(type=MessageType.PATIENT, content="Hola"),
        Message(type=MessageType.ASSISTANT, content="Hola, ¿cómo estás?"),
    ]


@pytest.fixture
def stored_conversation(active_patient: Patient, earlier_messages: list[Message]) -> Conversation:
    return Conversation(id=ConversationId.generate(), patient_id=active_patient.id, messages=earlier_messages)


@pytest.fixture
def reply() -> Message:
    return Message(type=MessageType.ASSISTANT, content="¿Desde cuándo te pasa?")


@pytest.fixture
def replies(reply: Message) -> list[Message]:
    return [
        Message(
            type=MessageType.ASSISTANT,
            content="",
            tool_calls=(ToolCall(id="call-1", name="find_sessions", arguments={"limit": 1}),),
        ),
        Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1"),
        reply,
    ]


@pytest.fixture
def conversations(stored_conversation: Conversation) -> SpyConversationCommandRepository:
    return SpyConversationCommandRepository(conversations=[stored_conversation])


@pytest.fixture
def start_conversation_handler(
    conversations: SpyConversationCommandRepository, repository: SpyPatientCommandRepository
) -> StartConversationCommandHandler:
    return StartConversationCommandHandler(conversations=conversations, patients=repository)


@pytest.fixture
def assistant(replies: list[Message]) -> SpyAssistant:
    return SpyAssistant(replies=replies)


@pytest.fixture
def talk_to_assistant_handler(
    conversations: SpyConversationCommandRepository, assistant: SpyAssistant
) -> TalkToAssistantCommandHandler:
    return TalkToAssistantCommandHandler(conversations=conversations, assistant=assistant)
