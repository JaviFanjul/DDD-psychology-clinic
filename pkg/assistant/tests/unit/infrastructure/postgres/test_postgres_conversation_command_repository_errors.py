import pytest
from assistant.domain.model.conversation.errors import ConversationNotLoaded, ConversationNotSaved
from assistant.infrastructure.postgres.postgres_conversation_command_repository import (
    PostgresConversationCommandRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_saving_then_it_rolls_back_and_raises_not_saved(
    failing_session, conversation
):
    repository = PostgresConversationCommandRepository(session=failing_session)

    with pytest.raises(ConversationNotSaved) as raised:
        await repository.save(conversation=conversation)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
    assert failing_session.rolled_back


async def test_given_a_failing_database_when_finding_then_it_raises_not_loaded(failing_session, conversation):
    repository = PostgresConversationCommandRepository(session=failing_session)

    with pytest.raises(ConversationNotLoaded) as raised:
        await repository.find_by_id(id=conversation.id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
