from uuid import UUID

import pytest
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.infrastructure.postgres.patient_model import PatientModel
from sqlalchemy.exc import SQLAlchemyError

ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


class FailingSession:
    def __init__(self) -> None:
        self.rolled_back = False

    async def merge(self, instance):
        raise SQLAlchemyError("database unavailable")

    async def rollback(self):
        self.rolled_back = True

    async def get(self, entity, ident):
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
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
    )
