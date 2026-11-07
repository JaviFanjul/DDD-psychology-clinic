from collections.abc import AsyncIterator, Iterator

import aio_pika
import pytest
from aio_pika import ExchangeType
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue
from core.domain.model.patient.events import (
    PatientCreated,
    PatientDischarged,
    PatientReadmitted,
)
from core.domain.model.patient.patient_id import PatientId
from core.infrastructure.rabbitmq.rabbitmq_event_bus import CORE_EXCHANGE, RabbitMqEventBus
from testcontainers.community.rabbitmq import RabbitMqContainer

RABBITMQ_IMAGE = "rabbitmq:4.2.1-alpine"


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
async def queue(channel: AbstractChannel, exchange: AbstractExchange) -> AbstractQueue:
    queue = await channel.declare_queue(exclusive=True)
    await queue.bind(exchange, routing_key="#")
    return queue


@pytest.fixture
def event_bus(exchange: AbstractExchange) -> RabbitMqEventBus:
    return RabbitMqEventBus(exchange=exchange)


@pytest.fixture
def events() -> list[PatientCreated | PatientDischarged | PatientReadmitted]:
    patient_id = PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7")
    return [
        PatientCreated(patient_id=patient_id),
        PatientDischarged(patient_id=patient_id),
        PatientReadmitted(patient_id=patient_id),
    ]
