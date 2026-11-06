import pytest
from assistant.application.command.talk_to_assistant import TalkToAssistantCommand
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import ConversationNotFound, ConversationNotOwned
from assistant.domain.model.conversation.message import Message, MessageType


async def test_given_its_patient_when_handling_then_it_returns_the_final_reply(
    talk_to_assistant_handler, stored_conversation, active_patient, reply
):
    result = await talk_to_assistant_handler.handle(
        command=TalkToAssistantCommand(
            conversation_id=stored_conversation.id,
            patient_id=active_patient.id,
            content="Me cuesta dormir",
        )
    )

    assert result == reply


async def test_given_its_patient_when_handling_then_the_assistant_gets_the_whole_conversation(
    talk_to_assistant_handler, assistant, stored_conversation, active_patient, earlier_messages
):
    await talk_to_assistant_handler.handle(
        command=TalkToAssistantCommand(
            conversation_id=stored_conversation.id,
            patient_id=active_patient.id,
            content="Me cuesta dormir",
        )
    )

    assert assistant.asked == [
        [*earlier_messages, Message(type=MessageType.PATIENT, content="Me cuesta dormir")]
    ]


async def test_given_its_patient_when_handling_then_the_message_and_all_replies_are_saved(
    talk_to_assistant_handler,
    conversations,
    stored_conversation,
    active_patient,
    earlier_messages,
    replies,
):
    await talk_to_assistant_handler.handle(
        command=TalkToAssistantCommand(
            conversation_id=stored_conversation.id,
            patient_id=active_patient.id,
            content="Me cuesta dormir",
        )
    )

    [conversation] = conversations.saved
    assert conversation.messages == [
        *earlier_messages,
        Message(type=MessageType.PATIENT, content="Me cuesta dormir"),
        *replies,
    ]


async def test_given_an_unknown_conversation_when_handling_then_it_raises_without_asking_or_saving(
    talk_to_assistant_handler, conversations, assistant, active_patient
):
    with pytest.raises(ConversationNotFound):
        await talk_to_assistant_handler.handle(
            command=TalkToAssistantCommand(
                conversation_id=ConversationId.generate(),
                patient_id=active_patient.id,
                content="Me cuesta dormir",
            )
        )

    assert assistant.asked == []
    assert conversations.saved == []


async def test_given_another_patient_when_handling_then_it_raises_without_asking_or_saving(
    talk_to_assistant_handler, conversations, assistant, stored_conversation, inactive_patient
):
    with pytest.raises(ConversationNotOwned):
        await talk_to_assistant_handler.handle(
            command=TalkToAssistantCommand(
                conversation_id=stored_conversation.id,
                patient_id=inactive_patient.id,
                content="Me cuesta dormir",
            )
        )

    assert assistant.asked == []
    assert conversations.saved == []
