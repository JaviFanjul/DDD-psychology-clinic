import pytest
from core.domain.command_bus import Command, CommandBus
from core.domain.model.patient.patient_query_repository import PatientDto
from core.domain.query_bus import Query, QueryBus
from core.entrypoint.patient.http.patient_controller import PatientController


class SpyCommandBus(CommandBus):
    def __init__(self) -> None:
        self.handled: list[Command] = []

    def handle(self, command: Command) -> None:
        self.handled.append(command)


class SpyQueryBus(QueryBus):
    def __init__(self, result: PatientDto) -> None:
        self._result = result
        self.handled: list[Query] = []

    def handle[TResult](self, query: Query[TResult]) -> TResult:
        self.handled.append(query)
        return self._result


@pytest.fixture
def create_data() -> dict[str, str]:
    return {
        "email": "ana@gmail.com",
        "first_name": "Ana",
        "last_names": "García López",
        "street": "Calle Mayor 3, 2º B",
        "postal_code": "08001",
        "city": "Barcelona",
        "province": "Barcelona",
    }


@pytest.fixture
def patient_dto() -> PatientDto:
    return PatientDto(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        email="ana@gmail.com",
        first_name="Ana",
        last_names="García López",
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
    )


@pytest.fixture
def command_bus() -> SpyCommandBus:
    return SpyCommandBus()


@pytest.fixture
def query_bus(patient_dto: PatientDto) -> SpyQueryBus:
    return SpyQueryBus(result=patient_dto)


@pytest.fixture
def controller(command_bus: SpyCommandBus, query_bus: SpyQueryBus) -> PatientController:
    return PatientController(command_bus=command_bus, query_bus=query_bus)
