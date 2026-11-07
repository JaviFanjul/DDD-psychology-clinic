from uuid import UUID

import pytest
from core.domain.model.psychologist.errors import InvalidPsychologistId
from core.domain.model.psychologist.psychologist_id import PsychologistId

A_UUID_STRING = "12345678-1234-4678-9234-567812345678"


def test_given_a_generated_id_when_generating_another_then_their_uuids_differ():
    first = PsychologistId.generate()

    second = PsychologistId.generate()

    assert first.id != second.id


def test_given_a_valid_string_when_parsing_then_it_holds_the_matching_uuid():
    valid_string = A_UUID_STRING

    psychologist_id = PsychologistId.from_string(id=valid_string)

    assert psychologist_id.id == UUID(valid_string)


def test_given_a_malformed_string_when_parsing_then_it_raises_invalid_psychologist_id():
    malformed_string = "not-a-uuid"

    with pytest.raises(InvalidPsychologistId):
        PsychologistId.from_string(id=malformed_string)


def test_given_a_psychologist_id_when_converting_to_string_then_it_returns_the_uuid_string():
    psychologist_id = PsychologistId.from_string(id=A_UUID_STRING)

    string = str(psychologist_id)

    assert string == A_UUID_STRING
