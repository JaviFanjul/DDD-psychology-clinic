from assistant.domain.model.conversation.conversation_query_repository import (
    ConversationDto,
    MessageDto,
)
from assistant.infrastructure.postgres.postgres_conversation_command_repository import (
    PostgresConversationCommandRepository,
)
from assistant.infrastructure.postgres.postgres_conversation_query_repository import (
    PostgresConversationQueryRepository,
)


async def find_by_id(sessions, id):
    async with sessions() as session:
        return await PostgresConversationQueryRepository(session=session).find_by_id(id=id)


async def test_given_a_saved_conversation_when_finding_it_then_it_returns_its_dto(
    sessions, conversation
):
    async with sessions() as session:
        await PostgresConversationCommandRepository(session=session).save(conversation=conversation)

    found = await find_by_id(sessions=sessions, id=conversation.id)

    assert found == ConversationDto(
        id="12345678-1234-4678-9234-567812345678",
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        messages=[
            MessageDto(type="patient", content="Me cuesta dormir"),
            MessageDto(type="assistant", content="¿Desde cuándo?"),
        ],
    )


async def test_given_no_conversation_with_that_id_when_finding_it_then_it_returns_none(
    sessions, unknown_conversation_id
):
    found = await find_by_id(sessions=sessions, id=unknown_conversation_id)

    assert found is None
