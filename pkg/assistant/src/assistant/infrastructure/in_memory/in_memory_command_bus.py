from typing import Any

from assistant.domain.command_bus import Command, CommandBus, CommandHandler


class InMemoryCommandBus(CommandBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Command[Any]], CommandHandler[Any, Any]] = {}

    def register[TCommand: Command[Any], TResult](
        self, command_type: type[TCommand], handler: CommandHandler[TCommand, TResult]
    ) -> None:
        self._handlers[command_type] = handler

    async def handle[TResult](self, command: Command[TResult]) -> TResult:
        result: TResult = await self._handlers[type(command)].handle(command=command)
        return result
