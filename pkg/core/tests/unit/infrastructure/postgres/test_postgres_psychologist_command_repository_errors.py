import pytest
from core.domain.model.psychologist.errors import PsychologistNotSaved
from core.infrastructure.postgres.postgres_psychologist_command_repository import (
    PostgresPsychologistCommandRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_saving_then_it_rolls_back_and_raises_not_saved(
    failing_session, psychologist
):
    repository = PostgresPsychologistCommandRepository(session=failing_session)

    with pytest.raises(PsychologistNotSaved) as raised:
        await repository.save(psychologist=psychologist)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
    assert failing_session.rolled_back
