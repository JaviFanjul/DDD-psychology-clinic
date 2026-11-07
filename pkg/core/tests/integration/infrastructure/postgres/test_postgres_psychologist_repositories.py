from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto
from core.infrastructure.postgres.postgres_psychologist_command_repository import (
    PostgresPsychologistCommandRepository,
)
from core.infrastructure.postgres.postgres_psychologist_query_repository import (
    PostgresPsychologistQueryRepository,
)


async def find_by_id(sessions, id):
    async with sessions() as session:
        return await PostgresPsychologistQueryRepository(session=session).find_by_id(id=id)


async def test_given_a_saved_psychologist_when_finding_it_then_it_returns_its_dto(sessions, psychologist):
    async with sessions() as session:
        await PostgresPsychologistCommandRepository(session=session).save(psychologist=psychologist)

    found = await find_by_id(sessions=sessions, id=psychologist.id)

    assert found == PsychologistDto(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )


async def test_given_no_psychologist_with_that_id_when_finding_it_then_it_returns_none(
    sessions, unknown_psychologist_id
):
    found = await find_by_id(sessions=sessions, id=unknown_psychologist_id)

    assert found is None
