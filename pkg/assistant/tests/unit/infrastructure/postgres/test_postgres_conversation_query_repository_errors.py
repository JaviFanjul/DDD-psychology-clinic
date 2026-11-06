import pytest
from assistant.domain.model.conversation.errors import ConversationNotLoaded
from assistant.infrastructure.postgres.postgres_conversation_query_repository import (
    PostgresConversationQueryRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_finding_then_it_raises_conversation_not_loaded(
    failing_session, conversation
):
    repository = PostgresConversationQueryRepository(session=failing_session)

    with pytest.raises(ConversationNotLoaded) as raised:
        await repository.find_by_id(id=conversation.id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
