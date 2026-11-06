from abc import ABC, abstractmethod

from assistant.domain.model.conversation.message import Message


class Assistant(ABC):
    @abstractmethod
    async def ask(self, messages: list[Message]) -> list[Message]: ...
