from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_command_repository import (
    ConversationCommandRepository,
)
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import ConversationNotLoaded, ConversationNotSaved
from assistant.infrastructure.postgres.conversation_mapper import ConversationMapper
from assistant.infrastructure.postgres.conversation_model import ConversationModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresConversationCommandRepository(ConversationCommandRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, conversation: Conversation) -> None:
        try:
            await self._session.merge(ConversationMapper.to_model(conversation=conversation))
            await self._session.commit()
        except SQLAlchemyError as error:
            await self._session.rollback()
            raise ConversationNotSaved(id=str(conversation.id)) from error

    async def find_by_id(self, id: ConversationId) -> Conversation | None:
        try:
            model = await self._session.get(ConversationModel, id.id)
        except SQLAlchemyError as error:
            raise ConversationNotLoaded(id=str(id)) from error
        if model is None:
            return None
        return ConversationMapper.to_entity(model=model)
