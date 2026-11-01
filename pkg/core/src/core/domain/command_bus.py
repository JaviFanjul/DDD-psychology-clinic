from abc import ABC, abstractmethod


class Command: ...


class CommandHandler[TCommand: Command](ABC):
    @abstractmethod
    def handle(self, command: TCommand) -> None: ...


class CommandBus(ABC):
    @abstractmethod
    def handle(self, command: Command) -> None: ...
