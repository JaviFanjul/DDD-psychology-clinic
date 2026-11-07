import pytest
from core.application.query.get_patient import GetPatientQueryHandler
from core.application.query.get_psychologist import GetPsychologistQueryHandler
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_query_repository import (
    PatientDto,
    PatientQueryRepository,
)
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_query_repository import (
    PsychologistDto,
    PsychologistQueryRepository,
)

KNOWN_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


class StubPatientQueryRepository(PatientQueryRepository):
    def __init__(self, patients: dict[PatientId, PatientDto]) -> None:
        self._patients = patients

    async def find_by_id(self, id: PatientId) -> PatientDto | None:
        return self._patients.get(id)


class StubPsychologistQueryRepository(PsychologistQueryRepository):
    def __init__(self, psychologists: dict[PsychologistId, PsychologistDto]) -> None:
        self._psychologists = psychologists

    async def find_by_id(self, id: PsychologistId) -> PsychologistDto | None:
        return self._psychologists.get(id)


@pytest.fixture
def known_id() -> str:
    return KNOWN_ID


@pytest.fixture
def known_patient(known_id: str) -> PatientDto:
    return PatientDto(
        id=known_id,
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
def handler(known_id: str, known_patient: PatientDto) -> GetPatientQueryHandler:
    repository = StubPatientQueryRepository(
        patients={PatientId.from_string(id=known_id): known_patient}
    )
    return GetPatientQueryHandler(repository=repository)


@pytest.fixture
def known_psychologist(known_id: str) -> PsychologistDto:
    return PsychologistDto(
        id=known_id,
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )


@pytest.fixture
def psychologist_handler(
    known_id: str, known_psychologist: PsychologistDto
) -> GetPsychologistQueryHandler:
    repository = StubPsychologistQueryRepository(
        psychologists={PsychologistId.from_string(id=known_id): known_psychologist}
    )
    return GetPsychologistQueryHandler(repository=repository)
