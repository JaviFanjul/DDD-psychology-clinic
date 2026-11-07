import pytest
from core.domain.model.psychologist.errors import PsychologistNotLoaded
from core.infrastructure.postgres.postgres_psychologist_query_repository import (
    PostgresPsychologistQueryRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_finding_then_it_raises_psychologist_not_loaded(
    failing_session, psychologist
):
    repository = PostgresPsychologistQueryRepository(session=failing_session)

    with pytest.raises(PsychologistNotLoaded) as raised:
        await repository.find_by_id(id=psychologist.id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
