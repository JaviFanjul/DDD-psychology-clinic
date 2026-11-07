import pytest
from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import ConversationNotOwned
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from assistant.domain.model.patient.patient_id import PatientId


def test_given_its_data_when_starting_then_the_conversation_holds_it_without_messages(conversation_id, patient_id):
    conversation = Conversation.start(id=conversation_id, patient_id=patient_id)

    assert conversation.id == conversation_id
    assert conversation.patient_id == patient_id
    assert conversation.messages == []


def test_given_its_patient_when_writing_then_the_conversation_records_the_message(conversation, patient_id):
    conversation.patient_writes(patient_id=patient_id, content="Me cuesta dormir")

    assert conversation.messages == [Message(type=MessageType.PATIENT, content="Me cuesta dormir")]


def test_given_another_patient_when_writing_then_it_raises_and_records_nothing(conversation):
    another_patient_id = PatientId.from_string(id="12345678-1234-4678-9234-567812345678")

    with pytest.raises(ConversationNotOwned):
        conversation.patient_writes(patient_id=another_patient_id, content="Me cuesta dormir")

    assert conversation.messages == []


def test_given_replies_when_the_assistant_replies_then_the_conversation_records_them_in_order(conversation, patient_id):
    conversation.patient_writes(patient_id=patient_id, content="Me cuesta dormir")
    replies = [
        Message(
            type=MessageType.ASSISTANT,
            content="",
            tool_calls=(ToolCall(id="call-1", name="find_sessions", arguments={"limit": 1}),),
        ),
        Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1"),
        Message(type=MessageType.ASSISTANT, content="¿Desde cuándo?"),
    ]

    conversation.assistant_replies(messages=replies)

    assert conversation.messages == [
        Message(type=MessageType.PATIENT, content="Me cuesta dormir"),
        *replies,
    ]


def test_given_two_conversations_with_the_same_id_when_comparing_then_they_are_equal(conversation, conversation_id):
    same_conversation = Conversation(
        id=conversation_id,
        patient_id=PatientId.from_string(id="12345678-1234-4678-9234-567812345678"),
        messages=[Message(type=MessageType.PATIENT, content="Hola")],
    )

    assert same_conversation == conversation
    assert hash(same_conversation) == hash(conversation)


def test_given_two_conversations_with_different_ids_when_comparing_then_they_are_not_equal(conversation, patient_id):
    other_conversation = Conversation.start(id=ConversationId.generate(), patient_id=patient_id)

    assert other_conversation != conversation
