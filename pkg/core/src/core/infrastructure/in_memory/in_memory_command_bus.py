from typing import Any

from core.domain.command_bus import Command, CommandBus, CommandHandler


class InMemoryCommandBus(CommandBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Command], CommandHandler[Any]] = {}

    def register[TCommand: Command](
        self, command_type: type[TCommand], handler: CommandHandler[TCommand]
    ) -> None:
        self._handlers[command_type] = handler

    async def handle(self, command: Command) -> None:
        await self._handlers[type(command)].handle(command=command)
