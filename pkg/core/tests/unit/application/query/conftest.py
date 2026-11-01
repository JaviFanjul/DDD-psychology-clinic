import pytest
from core.application.query.get_patient import GetPatientQueryHandler
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_query_repository import (
    PatientDto,
    PatientQueryRepository,
)

KNOWN_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


class StubPatientQueryRepository(PatientQueryRepository):
    def __init__(self, patients: dict[PatientId, PatientDto]) -> None:
        self._patients = patients

    def find_by_id(self, id: PatientId) -> PatientDto | None:
        return self._patients.get(id)


@pytest.fixture
def known_id() -> str:
    return KNOWN_ID


@pytest.fixture
def known_patient(known_id: str) -> PatientDto:
    return PatientDto(id=known_id, email="ana@gmail.com")


@pytest.fixture
def handler(known_id: str, known_patient: PatientDto) -> GetPatientQueryHandler:
    repository = StubPatientQueryRepository({PatientId.from_string(known_id): known_patient})
    return GetPatientQueryHandler(repository)
