import pytest
from core.domain.command_bus import Command, CommandHandler
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventHandler
from core.domain.query_bus import Query, QueryHandler
from core.infrastructure.in_memory.in_memory_command_bus import InMemoryCommandBus
from core.infrastructure.in_memory.in_memory_event_bus import InMemoryEventBus
from core.infrastructure.in_memory.in_memory_query_bus import InMemoryQueryBus


class FirstCommand(Command): ...


class SecondCommand(Command): ...


class SpyCommandHandler(CommandHandler[Command]):
    def __init__(self) -> None:
        self.handled: list[Command] = []

    async def handle(self, command: Command) -> None:
        self.handled.append(command)


class FirstEvent(DomainEvent): ...


class SecondEvent(DomainEvent): ...


class UnhandledEvent(DomainEvent): ...


class SpyEventHandler(EventHandler[DomainEvent]):
    def __init__(self) -> None:
        self.handled: list[DomainEvent] = []

    async def handle(self, event: DomainEvent) -> None:
        self.handled.append(event)


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
    return SpyCommandHandler()


@pytest.fixture
def second_handler() -> SpyCommandHandler:
    return SpyCommandHandler()


@pytest.fixture
def command_bus(
    first_handler: SpyCommandHandler, second_handler: SpyCommandHandler
) -> InMemoryCommandBus:
    bus = InMemoryCommandBus()
    bus.register(command_type=FirstCommand, handler=first_handler)
    bus.register(command_type=SecondCommand, handler=second_handler)
    return bus


@pytest.fixture
def first_event() -> FirstEvent:
    return FirstEvent()


@pytest.fixture
def second_event() -> SecondEvent:
    return SecondEvent()


@pytest.fixture
def unhandled_event() -> UnhandledEvent:
    return UnhandledEvent()


@pytest.fixture
def first_handler_of_first_event() -> SpyEventHandler:
    return SpyEventHandler()


@pytest.fixture
def second_handler_of_first_event() -> SpyEventHandler:
    return SpyEventHandler()


@pytest.fixture
def handler_of_second_event() -> SpyEventHandler:
    return SpyEventHandler()


@pytest.fixture
def event_bus(
    first_handler_of_first_event: SpyEventHandler,
    second_handler_of_first_event: SpyEventHandler,
    handler_of_second_event: SpyEventHandler,
) -> InMemoryEventBus:
    bus = InMemoryEventBus()
    bus.register(event_type=FirstEvent, handler=first_handler_of_first_event)
    bus.register(event_type=FirstEvent, handler=second_handler_of_first_event)
    bus.register(event_type=SecondEvent, handler=handler_of_second_event)
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
