from abc import ABC, abstractmethod
from dataclasses import dataclass

from assistant.domain.model.conversation.conversation_id import ConversationId


@dataclass(frozen=True)
class MessageDto:
    type: str
    content: str


@dataclass(frozen=True)
class ConversationDto:
    id: str
    patient_id: str
    messages: list[MessageDto]


class ConversationQueryRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: ConversationId) -> ConversationDto | None: ...
