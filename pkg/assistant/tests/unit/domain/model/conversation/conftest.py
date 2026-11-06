import pytest
from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.patient.patient_id import PatientId


@pytest.fixture
def conversation_id() -> ConversationId:
    return ConversationId.generate()


@pytest.fixture
def patient_id() -> PatientId:
    return PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7")


@pytest.fixture
def conversation(conversation_id: ConversationId, patient_id: PatientId) -> Conversation:
    return Conversation.start(id=conversation_id, patient_id=patient_id)
