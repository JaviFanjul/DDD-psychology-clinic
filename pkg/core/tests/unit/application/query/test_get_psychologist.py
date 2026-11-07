import pytest
from core.application.query.get_psychologist import GetPsychologistQuery
from core.domain.model.psychologist.errors import PsychologistNotFound
from core.domain.model.psychologist.psychologist_id import PsychologistId


async def test_given_a_known_id_when_handling_then_it_returns_the_psychologist(
    psychologist_handler, known_id, known_psychologist
):
    psychologist = await psychologist_handler.handle(
        query=GetPsychologistQuery(id=PsychologistId.from_string(id=known_id))
    )

    assert psychologist == known_psychologist


async def test_given_an_id_without_a_psychologist_when_handling_then_it_raises_not_found(
    psychologist_handler,
):
    with pytest.raises(PsychologistNotFound):
        await psychologist_handler.handle(query=GetPsychologistQuery(id=PsychologistId.generate()))
