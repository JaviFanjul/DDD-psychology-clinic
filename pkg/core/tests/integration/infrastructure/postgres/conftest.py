import time
from collections.abc import AsyncIterator, Iterator

import pytest
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone
from core.domain.model.patient.patient_status import PatientStatus
from core.infrastructure.postgres.base import Base
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
    return Patient(
        id=PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7"),
        email=PatientEmail(value="ana@gmail.com"),
        name=PatientName(first_name="Ana", last_names="García López"),
        phone=PatientPhone(prefix="+34", number="612345678"),
        address=PatientAddress(
            street="Calle Mayor 3, 2º B",
            postal_code="08001",
            city="Barcelona",
            province="Barcelona",
        ),
        status=PatientStatus.ACTIVE,
    )


@pytest.fixture
def unknown_id() -> PatientId:
    return PatientId.from_string(id="00000000-0000-4000-8000-000000000000")
