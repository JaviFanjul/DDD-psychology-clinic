import asyncio
from collections.abc import AsyncIterator, Callable, Iterator

import aio_pika
import pytest
from aio_pika import ExchangeType
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventHandler
from core.domain.model.appointment.appointment_id import AppointmentId
from core.entrypoint.appointment.rabbitmq.appointment_event_consumer import (
    CORE_EXCHANGE,
    EVENT_BY_ROUTING_KEY,
    AppointmentEventConsumer,
)
from core.infrastructure.rabbitmq.rabbitmq_event_bus import RabbitMqEventBus
from testcontainers.community.rabbitmq import RabbitMqContainer

RABBITMQ_IMAGE = "rabbitmq:4.2.1-alpine"
WAIT_TIMEOUT_SECONDS = 5


class SpyEventHandler(EventHandler[DomainEvent]):
    def __init__(self) -> None:
        self.handled: list[DomainEvent] = []

    async def handle(self, event: DomainEvent) -> None:
        self.handled.append(event)


class FailingOnceEventHandler(EventHandler[DomainEvent]):
    def __init__(self) -> None:
        self.handled: list[DomainEvent] = []

    async def handle(self, event: DomainEvent) -> None:
        self.handled.append(event)
        if len(self.handled) == 1:
            raise RuntimeError("database unavailable")


@pytest.fixture(scope="session")
def rabbitmq_url() -> Iterator[str]:
    with RabbitMqContainer(image=RABBITMQ_IMAGE) as rabbitmq:
        host = rabbitmq.get_container_host_ip()
        port = rabbitmq.get_exposed_port(rabbitmq.port)
        yield f"amqp://{rabbitmq.username}:{rabbitmq.password}@{host}:{port}/"


@pytest.fixture
async def channel(rabbitmq_url: str) -> AsyncIterator[AbstractChannel]:
    connection = await aio_pika.connect(rabbitmq_url)
    yield await connection.channel()
    await connection.close()


@pytest.fixture
async def exchange(channel: AbstractChannel) -> AbstractExchange:
    return await channel.declare_exchange(name=CORE_EXCHANGE, type=ExchangeType.TOPIC, durable=True)


@pytest.fixture
async def queue(channel: AbstractChannel, exchange: AbstractExchange) -> AsyncIterator[AbstractQueue]:
    queue = await channel.declare_queue(exclusive=True)
    for routing_key in EVENT_BY_ROUTING_KEY:
        await queue.bind(exchange=exchange, routing_key=routing_key)
    yield queue
    await queue.delete(if_unused=False, if_empty=False)


@pytest.fixture
def consume(queue: AbstractQueue) -> Callable:
    async def start(handler: EventHandler[DomainEvent]) -> None:
        await queue.consume(AppointmentEventConsumer(handler=handler).consume)

    return start


@pytest.fixture
def event_bus(exchange: AbstractExchange) -> RabbitMqEventBus:
    return RabbitMqEventBus(exchange=exchange)


@pytest.fixture
def wait_until() -> Callable:
    async def wait(condition: Callable[[], bool]) -> None:
        async with asyncio.timeout(WAIT_TIMEOUT_SECONDS):
            while not condition():
                await asyncio.sleep(0.05)

    return wait


@pytest.fixture
def appointment_id() -> AppointmentId:
    return AppointmentId.from_string(id="3f2504e0-4f89-41d3-9a0c-0305e82c3301")


@pytest.fixture
def handler() -> SpyEventHandler:
    return SpyEventHandler()


@pytest.fixture
def failing_once_handler() -> FailingOnceEventHandler:
    return FailingOnceEventHandler()
