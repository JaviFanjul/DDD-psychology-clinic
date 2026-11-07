import pytest
from assistant.domain.model.conversation.errors import (
    AssistantNotAnswered,
    ConversationNotFound,
    ConversationNotLoaded,
    ConversationNotOwned,
    ConversationNotSaved,
    InvalidConversationId,
)


def test_given_a_malformed_value_when_creating_invalid_conversation_id_then_its_message_names_it():
    malformed_value = "not-a-uuid"

    error = InvalidConversationId(value=malformed_value)

    assert str(error) == "'not-a-uuid' is not a valid UUID"


@pytest.mark.parametrize(
    ("error_type", "expected_message"),
    [
        (ConversationNotFound, "Conversation 'some-id' was not found"),
        (ConversationNotSaved, "Conversation 'some-id' could not be saved"),
        (ConversationNotLoaded, "Conversation 'some-id' could not be loaded"),
    ],
)
def test_given_an_id_when_creating_a_conversation_error_then_its_message_names_it(error_type, expected_message):
    id = "some-id"

    error = error_type(id=id)

    assert str(error) == expected_message


def test_given_an_id_and_a_patient_when_creating_conversation_not_owned_then_it_names_them():
    id = "some-id"
    patient_id = "some-patient-id"

    error = ConversationNotOwned(id=id, patient_id=patient_id)

    assert str(error) == "Conversation 'some-id' does not belong to patient 'some-patient-id'"


def test_given_nothing_when_creating_assistant_not_answered_then_its_message_explains_it():
    error = AssistantNotAnswered()

    assert str(error) == "The assistant could not answer"
