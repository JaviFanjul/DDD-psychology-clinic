import pytest
from assistant.application.query.get_conversation import GetConversationQuery
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import ConversationNotFound


async def test_given_a_known_id_when_handling_then_it_returns_the_conversation(
    handler, known_id, known_conversation
):
    conversation = await handler.handle(
        query=GetConversationQuery(id=ConversationId.from_string(id=known_id))
    )

    assert conversation == known_conversation


async def test_given_an_id_without_a_conversation_when_handling_then_it_raises_not_found(
    handler,
):
    with pytest.raises(ConversationNotFound):
        await handler.handle(query=GetConversationQuery(id=ConversationId.generate()))
