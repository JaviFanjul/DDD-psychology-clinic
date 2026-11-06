from abc import ABC, abstractmethod

from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_id import ConversationId


class ConversationCommandRepository(ABC):
    @abstractmethod
    async def save(self, conversation: Conversation) -> None: ...

    @abstractmethod
    async def find_by_id(self, id: ConversationId) -> Conversation | None: ...
