import time
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime

import pytest
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone
from core.domain.model.patient.patient_status import PatientStatus
from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone
from core.infrastructure.postgres.base import Base
from core.infrastructure.postgres.postgres_patient_command_repository import (
    PostgresPatientCommandRepository,
)
from core.infrastructure.postgres.postgres_psychologist_command_repository import (
    PostgresPsychologistCommandRepository,
)
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


@pytest.fixture
def psychologist() -> Psychologist:
    return Psychologist(
        id=PsychologistId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7"),
        email=PsychologistEmail(value="laura@clinica.es"),
        name=PsychologistName(first_name="Laura", last_names="Martín Ruiz"),
        phone=PsychologistPhone(prefix="+34", number="687654321"),
        license_number=PsychologistLicenseNumber(value="M-12345"),
    )


@pytest.fixture
def unknown_psychologist_id() -> PsychologistId:
    return PsychologistId.from_string(id="00000000-0000-4000-8000-000000000000")


@pytest.fixture
async def attendees(
    sessions: async_sessionmaker[AsyncSession], patient: Patient, psychologist: Psychologist
) -> tuple[Patient, Psychologist]:
    async with sessions() as session:
        await PostgresPatientCommandRepository(session=session).save(patient=patient)
        await PostgresPsychologistCommandRepository(session=session).save(psychologist=psychologist)
    return patient, psychologist


@pytest.fixture
def slot() -> AppointmentSlot:
    return AppointmentSlot(starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC), duration_minutes=50)


@pytest.fixture
def appointment(attendees: tuple[Patient, Psychologist], slot: AppointmentSlot) -> Appointment:
    patient, psychologist = attendees
    return Appointment(
        id=AppointmentId.from_string(id="3f2504e0-4f89-41d3-9a0c-0305e82c3301"),
        patient_id=patient.id,
        psychologist_id=psychologist.id,
        slot=slot,
        modality=AppointmentModality.ONLINE,
        status=AppointmentStatus.PENDING,
    )


@pytest.fixture
def unknown_appointment_id() -> AppointmentId:
    return AppointmentId.from_string(id="00000000-0000-4000-8000-000000000000")
