from abc import ABC, abstractmethod


class Command: ...


class CommandHandler[TCommand: Command](ABC):
    @abstractmethod
    async def handle(self, command: TCommand) -> None: ...


class CommandBus(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> None: ...
