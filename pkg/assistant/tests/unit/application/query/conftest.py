import pytest
from assistant.application.query.get_conversation import GetConversationQueryHandler
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.conversation_query_repository import (
    ConversationDto,
    ConversationQueryRepository,
    MessageDto,
)

KNOWN_ID = "12345678-1234-4678-9234-567812345678"


class StubConversationQueryRepository(ConversationQueryRepository):
    def __init__(self, conversations: dict[ConversationId, ConversationDto]) -> None:
        self._conversations = conversations

    async def find_by_id(self, id: ConversationId) -> ConversationDto | None:
        return self._conversations.get(id)


@pytest.fixture
def known_id() -> str:
    return KNOWN_ID


@pytest.fixture
def known_conversation(known_id: str) -> ConversationDto:
    return ConversationDto(
        id=known_id,
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        messages=[
            MessageDto(type="patient", content="Me cuesta dormir"),
            MessageDto(type="assistant", content="¿Desde cuándo?"),
        ],
    )


@pytest.fixture
def handler(known_id: str, known_conversation: ConversationDto) -> GetConversationQueryHandler:
    repository = StubConversationQueryRepository(
        conversations={ConversationId.from_string(id=known_id): known_conversation}
    )
    return GetConversationQueryHandler(repository=repository)
