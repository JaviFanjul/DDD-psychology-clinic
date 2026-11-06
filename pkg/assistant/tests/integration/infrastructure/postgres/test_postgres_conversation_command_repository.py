from assistant.domain.model.conversation.message import Message, MessageType
from assistant.infrastructure.postgres.postgres_conversation_command_repository import (
    PostgresConversationCommandRepository,
)


async def save(sessions, conversation):
    async with sessions() as session:
        await PostgresConversationCommandRepository(session=session).save(conversation=conversation)


async def find_by_id(sessions, id):
    async with sessions() as session:
        return await PostgresConversationCommandRepository(session=session).find_by_id(id=id)


async def test_given_a_saved_conversation_when_finding_it_then_it_returns_it(
    sessions, conversation
):
    await save(sessions=sessions, conversation=conversation)

    found = await find_by_id(sessions=sessions, id=conversation.id)

    assert found.id == conversation.id
    assert found.patient_id == conversation.patient_id
    assert found.messages == conversation.messages


async def test_given_a_saved_conversation_when_saving_new_messages_then_it_returns_them_in_order(
    sessions, conversation, patient
):
    await save(sessions=sessions, conversation=conversation)
    conversation.patient_writes(patient_id=patient.id, content="Desde hace un mes")
    conversation.assistant_replies(
        messages=[
            Message(type=MessageType.ASSISTANT, content="¿Qué cambió hace un mes?"),
        ]
    )

    await save(sessions=sessions, conversation=conversation)

    found = await find_by_id(sessions=sessions, id=conversation.id)
    assert found.messages == conversation.messages


async def test_given_no_conversation_with_that_id_when_finding_it_then_it_returns_none(
    sessions, unknown_conversation_id
):
    found = await find_by_id(sessions=sessions, id=unknown_conversation_id)

    assert found is None
