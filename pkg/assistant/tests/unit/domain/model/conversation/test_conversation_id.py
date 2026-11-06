from uuid import UUID

import pytest
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import InvalidConversationId

A_UUID_STRING = "12345678-1234-4678-9234-567812345678"


def test_given_a_generated_id_when_generating_another_then_their_uuids_differ():
    first = ConversationId.generate()

    second = ConversationId.generate()

    assert first.id != second.id


def test_given_a_valid_string_when_parsing_then_it_holds_the_matching_uuid():
    valid_string = A_UUID_STRING

    conversation_id = ConversationId.from_string(id=valid_string)

    assert conversation_id.id == UUID(valid_string)


def test_given_a_malformed_string_when_parsing_then_it_raises_invalid_conversation_id():
    malformed_string = "not-a-uuid"

    with pytest.raises(InvalidConversationId):
        ConversationId.from_string(id=malformed_string)


def test_given_a_conversation_id_when_converting_to_string_then_it_returns_the_uuid_string():
    conversation_id = ConversationId.from_string(id=A_UUID_STRING)

    string = str(conversation_id)

    assert string == A_UUID_STRING
