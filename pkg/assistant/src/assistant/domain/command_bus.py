from abc import ABC, abstractmethod
from typing import Any


class Command[TResult]: ...


class CommandHandler[TCommand: Command[Any], TResult](ABC):
    @abstractmethod
    async def handle(self, command: TCommand) -> TResult: ...


class CommandBus(ABC):
    @abstractmethod
    async def handle[TResult](self, command: Command[TResult]) -> TResult: ...
