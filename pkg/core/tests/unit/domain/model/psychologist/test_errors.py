import pytest
from core.domain.model.psychologist.errors import (
    InvalidPsychologistId,
    PsychologistNotFound,
    PsychologistNotLoaded,
    PsychologistNotNotified,
    PsychologistNotSaved,
)


def test_given_a_malformed_value_when_creating_invalid_psychologist_id_then_its_message_names_it():
    malformed_value = "not-a-uuid"

    error = InvalidPsychologistId(value=malformed_value)

    assert str(error) == "'not-a-uuid' is not a valid UUID"


@pytest.mark.parametrize(
    ("error_type", "expected_message"),
    [
        (PsychologistNotFound, "Psychologist 'some-id' was not found"),
        (PsychologistNotSaved, "Psychologist 'some-id' could not be saved"),
        (PsychologistNotLoaded, "Psychologist 'some-id' could not be loaded"),
        (PsychologistNotNotified, "Psychologist 'some-id' could not be notified"),
    ],
)
def test_given_an_id_when_creating_an_error_then_its_message_names_it(error_type, expected_message):
    id = "some-id"

    error = error_type(id=id)

    assert str(error) == expected_message
