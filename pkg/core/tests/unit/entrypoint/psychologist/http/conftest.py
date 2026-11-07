import pytest
from core.domain.command_bus import Command, CommandBus
from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto
from core.domain.query_bus import Query, QueryBus
from core.entrypoint.psychologist.http.psychologist_controller import PsychologistController


class SpyCommandBus(CommandBus):
    def __init__(self) -> None:
        self.handled: list[Command] = []

    async def handle(self, command: Command) -> None:
        self.handled.append(command)


class SpyQueryBus(QueryBus):
    def __init__(self, result: PsychologistDto) -> None:
        self._result = result
        self.handled: list[Query] = []

    async def handle[TResult](self, query: Query[TResult]) -> TResult:
        self.handled.append(query)
        return self._result


@pytest.fixture
def create_data() -> dict[str, str]:
    return {
        "email": "laura@clinica.es",
        "first_name": "Laura",
        "last_names": "Martín Ruiz",
        "phone_prefix": "+34",
        "phone_number": "687 65 43 21",
        "license_number": "m12345",
    }


@pytest.fixture
def psychologist_dto() -> PsychologistDto:
    return PsychologistDto(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )


@pytest.fixture
def command_bus() -> SpyCommandBus:
    return SpyCommandBus()


@pytest.fixture
def query_bus(psychologist_dto: PsychologistDto) -> SpyQueryBus:
    return SpyQueryBus(result=psychologist_dto)


@pytest.fixture
def controller(command_bus: SpyCommandBus, query_bus: SpyQueryBus) -> PsychologistController:
    return PsychologistController(command_bus=command_bus, query_bus=query_bus)
