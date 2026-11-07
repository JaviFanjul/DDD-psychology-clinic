import asyncio
import json
from collections.abc import AsyncIterator, Callable, Iterator

import aio_pika
import pytest
from aio_pika import ExchangeType, Message
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractQueue,
)
from assistant.entrypoint.patient.rabbitmq.patient_event_consumer import (
    COMMAND_BY_ROUTING_KEY,
    CORE_EXCHANGE,
    PatientEventConsumer,
)
from testcontainers.community.rabbitmq import RabbitMqContainer

RABBITMQ_IMAGE = "rabbitmq:4.2.1-alpine"
WAIT_TIMEOUT_SECONDS = 5


class SpyCommandBus:
    def __init__(self) -> None:
        self.handled: list = []

    async def handle(self, command):
        self.handled.append(command)


class FailingOnceCommandBus:
    def __init__(self) -> None:
        self.handled: list = []

    async def handle(self, command):
        self.handled.append(command)
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
    for routing_key in COMMAND_BY_ROUTING_KEY:
        await queue.bind(exchange=exchange, routing_key=routing_key)
    yield queue
    await queue.delete(if_unused=False, if_empty=False)


@pytest.fixture
def consume(queue: AbstractQueue) -> Callable:
    async def start(command_bus) -> None:
        await queue.consume(PatientEventConsumer(command_bus=command_bus).consume)

    return start


@pytest.fixture
def publish(exchange: AbstractExchange) -> Callable:
    async def send(routing_key: str, patient_id: str) -> None:
        body = {"patient_id": patient_id, "created_at": "2026-11-06T10:30:00+00:00"}
        await exchange.publish(
            message=Message(body=json.dumps(body).encode(), content_type="application/json"),
            routing_key=routing_key,
        )

    return send


@pytest.fixture
def wait_until() -> Callable:
    async def wait(condition: Callable[[], bool]) -> None:
        async with asyncio.timeout(WAIT_TIMEOUT_SECONDS):
            while not condition():
                await asyncio.sleep(0.05)

    return wait


@pytest.fixture
def patient_id() -> str:
    return "7c9e6679-7425-40de-944b-e07fc1f90ae7"


@pytest.fixture
def command_bus() -> SpyCommandBus:
    return SpyCommandBus()


@pytest.fixture
def failing_once_command_bus() -> FailingOnceCommandBus:
    return FailingOnceCommandBus()
