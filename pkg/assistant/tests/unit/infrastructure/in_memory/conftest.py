import pytest
from assistant.domain.command_bus import Command, CommandHandler
from assistant.domain.query_bus import Query, QueryHandler
from assistant.infrastructure.in_memory.in_memory_command_bus import InMemoryCommandBus
from assistant.infrastructure.in_memory.in_memory_query_bus import InMemoryQueryBus


class FirstCommand(Command[str]): ...


class SecondCommand(Command[str]): ...


class SpyCommandHandler(CommandHandler[Command[str], str]):
    def __init__(self, result: str) -> None:
        self._result = result
        self.handled: list[Command[str]] = []

    async def handle(self, command: Command[str]) -> str:
        self.handled.append(command)
        return self._result


class FirstQuery(Query[str]): ...


class SecondQuery(Query[str]): ...


class StubQueryHandler(QueryHandler[Query[str], str]):
    def __init__(self, result: str) -> None:
        self._result = result

    async def handle(self, query: Query[str]) -> str:
        return self._result


@pytest.fixture
def first_command() -> FirstCommand:
    return FirstCommand()


@pytest.fixture
def first_handler() -> SpyCommandHandler:
    return SpyCommandHandler(result="first result")


@pytest.fixture
def second_handler() -> SpyCommandHandler:
    return SpyCommandHandler(result="second result")


@pytest.fixture
def command_bus(
    first_handler: SpyCommandHandler, second_handler: SpyCommandHandler
) -> InMemoryCommandBus:
    bus = InMemoryCommandBus()
    bus.register(command_type=FirstCommand, handler=first_handler)
    bus.register(command_type=SecondCommand, handler=second_handler)
    return bus


@pytest.fixture
def first_query() -> FirstQuery:
    return FirstQuery()


@pytest.fixture
def query_bus() -> InMemoryQueryBus:
    bus = InMemoryQueryBus()
    bus.register(query_type=FirstQuery, handler=StubQueryHandler(result="first result"))
    bus.register(query_type=SecondQuery, handler=StubQueryHandler(result="second result"))
    return bus
