from core.domain.command_bus import Command, CommandBus, CommandHandler


class InMemoryCommandBus(CommandBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Command], CommandHandler] = {}

    def register[TCommand: Command](
        self, command_type: type[TCommand], handler: CommandHandler[TCommand]
    ) -> None:
        self._handlers[command_type] = handler

    def handle(self, command: Command) -> None:
        self._handlers[type(command)].handle(command)
