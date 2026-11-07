import json
from collections.abc import Callable
from contextlib import asynccontextmanager
from datetime import UTC, datetime

import pytest
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventHandler
from core.entrypoint.appointment.rabbitmq.appointment_event_consumer import AppointmentEventConsumer


class SpyEventHandler(EventHandler[DomainEvent]):
    def __init__(self) -> None:
        self.handled: list[DomainEvent] = []

    async def handle(self, event: DomainEvent) -> None:
        self.handled.append(event)


class FakeMessage:
    def __init__(self, routing_key: str, body: bytes) -> None:
        self.routing_key = routing_key
        self.body = body

    @asynccontextmanager
    async def process(self, requeue: bool):
        yield


@pytest.fixture
def created_at() -> datetime:
    return datetime(year=2026, month=11, day=6, hour=10, minute=30, tzinfo=UTC)


@pytest.fixture
def message(created_at: datetime) -> Callable[..., FakeMessage]:
    def build(routing_key: str, appointment_id: str) -> FakeMessage:
        body = {"appointment_id": appointment_id, "created_at": created_at.isoformat()}
        return FakeMessage(routing_key=routing_key, body=json.dumps(body).encode())

    return build


@pytest.fixture
def appointment_id() -> str:
    return "3f2504e0-4f89-41d3-9a0c-0305e82c3301"


@pytest.fixture
def handler() -> SpyEventHandler:
    return SpyEventHandler()


@pytest.fixture
def consumer(handler: SpyEventHandler) -> AppointmentEventConsumer:
    return AppointmentEventConsumer(handler=handler)
