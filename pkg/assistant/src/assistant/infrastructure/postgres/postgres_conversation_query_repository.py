from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.conversation_query_repository import (
    ConversationDto,
    ConversationQueryRepository,
)
from assistant.domain.model.conversation.errors import ConversationNotLoaded
from assistant.infrastructure.postgres.conversation_mapper import ConversationMapper
from assistant.infrastructure.postgres.conversation_model import ConversationModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresConversationQueryRepository(ConversationQueryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, id: ConversationId) -> ConversationDto | None:
        try:
            model = await self._session.get(ConversationModel, id.id)
        except SQLAlchemyError as error:
            raise ConversationNotLoaded(id=str(id)) from error
        if model is None:
            return None
        return ConversationMapper.to_dto(model=model)
