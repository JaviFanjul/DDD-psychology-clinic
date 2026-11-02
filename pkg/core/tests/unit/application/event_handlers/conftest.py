import pytest
from core.application.event_handlers.welcome_patient_on_patient_created import (
    WelcomePatientOnPatientCreated,
)
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_notifier import PatientNotifier
from core.domain.model.patient.patient_query_repository import (
    PatientDto,
    PatientQueryRepository,
)

KNOWN_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


class StubPatientQueryRepository(PatientQueryRepository):
    def __init__(self, patients: dict[PatientId, PatientDto]) -> None:
        self._patients = patients

    async def find_by_id(self, id: PatientId) -> PatientDto | None:
        return self._patients.get(id)


class SpyPatientNotifier(PatientNotifier):
    def __init__(self) -> None:
        self.welcomed: list[PatientDto] = []

    async def welcome(self, patient: PatientDto) -> None:
        self.welcomed.append(patient)


@pytest.fixture
def known_id() -> PatientId:
    return PatientId.from_string(id=KNOWN_ID)


@pytest.fixture
def known_patient() -> PatientDto:
    return PatientDto(
        id=KNOWN_ID,
        email="ana@gmail.com",
        first_name="Ana",
        last_names="García López",
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
    )


@pytest.fixture
def notifier() -> SpyPatientNotifier:
    return SpyPatientNotifier()


@pytest.fixture
def handler(
    known_id: PatientId, known_patient: PatientDto, notifier: SpyPatientNotifier
) -> WelcomePatientOnPatientCreated:
    repository = StubPatientQueryRepository(patients={known_id: known_patient})
    return WelcomePatientOnPatientCreated(repository=repository, notifier=notifier)
