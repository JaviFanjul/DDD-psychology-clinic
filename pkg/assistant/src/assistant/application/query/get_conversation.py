from dataclasses import dataclass

from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.conversation_query_repository import (
    ConversationDto,
    ConversationQueryRepository,
)
from assistant.domain.model.conversation.errors import ConversationNotFound
from assistant.domain.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetConversationQuery(Query[ConversationDto]):
    id: ConversationId


class GetConversationQueryHandler(QueryHandler[GetConversationQuery, ConversationDto]):
    def __init__(self, repository: ConversationQueryRepository) -> None:
        self._repository = repository

    async def handle(self, query: GetConversationQuery) -> ConversationDto:
        conversation: ConversationDto | None = await self._repository.find_by_id(id=query.id)
        if conversation is None:
            raise ConversationNotFound(id=str(query.id))
        return conversation
