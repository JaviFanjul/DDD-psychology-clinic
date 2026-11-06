from dataclasses import dataclass
from uuid import UUID, uuid4

from assistant.domain.model.conversation.errors import InvalidConversationId


@dataclass(frozen=True)
class ConversationId:
    id: UUID

    @classmethod
    def generate(cls) -> ConversationId:
        return cls(id=uuid4())

    @classmethod
    def from_string(cls, id: str) -> ConversationId:
        try:
            return cls(id=UUID(id))
        except ValueError as error:
            raise InvalidConversationId(value=id) from error

    def __str__(self) -> str:
        return str(self.id)
