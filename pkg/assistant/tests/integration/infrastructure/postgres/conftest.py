import time
from collections.abc import AsyncIterator, Iterator

import pytest
from assistant.domain.model.conversation.conversation import Conversation
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_id import PatientId
from assistant.infrastructure.postgres.base import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.community.postgres import PostgresContainer

POSTGRES_IMAGE = "postgres:18.6-alpine"
SCHEMA_TIMEOUT_SECONDS = 30


def create_schema(url: str) -> None:
    deadline = time.monotonic() + SCHEMA_TIMEOUT_SECONDS
    engine = create_engine(url)
    try:
        while True:
            try:
                Base.metadata.create_all(engine)
                return
            except OperationalError:
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.5)
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def database_url() -> Iterator[str]:
    with PostgresContainer(image=POSTGRES_IMAGE, driver="psycopg") as postgres:
        url = postgres.get_connection_url()
        create_schema(url=url)
        yield url


@pytest.fixture
async def sessions(database_url: str) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(database_url)
    yield async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            await connection.execute(table.delete())
    await engine.dispose()


@pytest.fixture
def patient() -> Patient:
    return Patient.create(id=PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7"))


@pytest.fixture
def conversation(patient: Patient) -> Conversation:
    return Conversation(
        id=ConversationId.from_string(id="12345678-1234-4678-9234-567812345678"),
        patient_id=patient.id,
        messages=[
            Message(type=MessageType.PATIENT, content="Me cuesta dormir"),
            Message(
                type=MessageType.ASSISTANT,
                content="",
                tool_calls=(ToolCall(id="call-1", name="find_sessions", arguments={"limit": 1}),),
            ),
            Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1"),
            Message(type=MessageType.ASSISTANT, content="¿Desde cuándo?"),
        ],
    )


@pytest.fixture
def unknown_patient_id() -> PatientId:
    return PatientId.from_string(id="00000000-0000-4000-8000-000000000000")


@pytest.fixture
def unknown_conversation_id() -> ConversationId:
    return ConversationId.from_string(id="00000000-0000-4000-8000-000000000000")
