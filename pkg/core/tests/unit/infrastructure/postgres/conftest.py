from datetime import UTC, datetime
from uuid import UUID

import pytest
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone
from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone
from core.infrastructure.postgres.appointment_model import AppointmentModel
from core.infrastructure.postgres.patient_model import PatientModel
from core.infrastructure.postgres.psychologist_model import PsychologistModel
from sqlalchemy.exc import SQLAlchemyError

ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"
PSYCHOLOGIST_ID = "0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
APPOINTMENT_ID = "3f2504e0-4f89-41d3-9a0c-0305e82c3301"
STARTS_AT = datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC)


class FailingSession:
    def __init__(self) -> None:
        self.rolled_back = False

    async def merge(self, instance):
        raise SQLAlchemyError("database unavailable")

    async def commit(self):
        raise SQLAlchemyError("database unavailable")

    async def rollback(self):
        self.rolled_back = True

    async def get(self, entity, ident):
        raise SQLAlchemyError("database unavailable")

    async def execute(self, statement):
        raise SQLAlchemyError("database unavailable")

    async def scalars(self, statement):
        raise SQLAlchemyError("database unavailable")


@pytest.fixture
def failing_session() -> FailingSession:
    return FailingSession()


@pytest.fixture
def patient() -> Patient:
    return Patient.create(
        id=PatientId.from_string(id=ID),
        email=PatientEmail(value="ana@gmail.com"),
        name=PatientName(first_name="Ana", last_names="García López"),
        phone=PatientPhone(prefix="+34", number="612345678"),
        address=PatientAddress(
            street="Calle Mayor 3, 2º B",
            postal_code="08001",
            city="Barcelona",
            province="Barcelona",
        ),
    )


@pytest.fixture
def model() -> PatientModel:
    return PatientModel(
        id=UUID(ID),
        email="ana@gmail.com",
        first_name="Ana",
        last_names="García López",
        phone_prefix="+34",
        phone_number="612345678",
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
        status="active",
    )


@pytest.fixture
def psychologist() -> Psychologist:
    return Psychologist.create(
        id=PsychologistId.from_string(id=ID),
        email=PsychologistEmail(value="laura@clinica.es"),
        name=PsychologistName(first_name="Laura", last_names="Martín Ruiz"),
        phone=PsychologistPhone(prefix="+34", number="687654321"),
        license_number=PsychologistLicenseNumber(value="M-12345"),
    )


@pytest.fixture
def psychologist_model() -> PsychologistModel:
    return PsychologistModel(
        id=UUID(ID),
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )


@pytest.fixture
def appointment() -> Appointment:
    return Appointment.schedule(
        id=AppointmentId.from_string(id=APPOINTMENT_ID),
        patient_id=PatientId.from_string(id=ID),
        psychologist_id=PsychologistId.from_string(id=PSYCHOLOGIST_ID),
        slot=AppointmentSlot(starts_at=STARTS_AT, duration_minutes=50),
        modality=AppointmentModality.ONLINE,
    )


@pytest.fixture
def appointment_model() -> AppointmentModel:
    return AppointmentModel(
        id=UUID(APPOINTMENT_ID),
        patient_id=UUID(ID),
        psychologist_id=UUID(PSYCHOLOGIST_ID),
        starts_at=STARTS_AT,
        duration_minutes=50,
        modality="online",
        status="pending",
    )
