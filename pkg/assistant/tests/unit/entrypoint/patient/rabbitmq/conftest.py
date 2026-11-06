import json
from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any

import pytest
from assistant.domain.command_bus import Command, CommandBus
from assistant.entrypoint.patient.rabbitmq.patient_event_consumer import PatientEventConsumer

PATIENT_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


class SpyCommandBus(CommandBus):
    def __init__(self) -> None:
        self.handled: list[Command[Any]] = []

    async def handle(self, command):
        self.handled.append(command)


class FakeMessage:
    def __init__(self, routing_key: str, body: bytes) -> None:
        self.routing_key = routing_key
        self.body = body

    @asynccontextmanager
    async def process(self, requeue: bool):
        yield


@pytest.fixture
def message() -> Callable[..., FakeMessage]:
    def build(routing_key: str, patient_id: str) -> FakeMessage:
        return FakeMessage(
            routing_key=routing_key, body=json.dumps({"patient_id": patient_id}).encode()
        )

    return build


@pytest.fixture
def patient_id() -> str:
    return PATIENT_ID


@pytest.fixture
def command_bus() -> SpyCommandBus:
    return SpyCommandBus()


@pytest.fixture
def consumer(command_bus: SpyCommandBus) -> PatientEventConsumer:
    return PatientEventConsumer(command_bus=command_bus)
