import pytest
from core.domain.model.psychologist.errors import InvalidPsychologistName
from core.domain.model.psychologist.psychologist_name import PsychologistName


@pytest.mark.parametrize(
    ("first_name", "last_names"),
    [
        ("", "Martín Ruiz"),
        ("   ", "Martín Ruiz"),
        ("Laura", ""),
        ("Laura", "   "),
    ],
)
def test_given_a_blank_part_when_creating_then_it_raises_invalid_psychologist_name(
    first_name, last_names
):
    with pytest.raises(InvalidPsychologistName):
        PsychologistName(first_name=first_name, last_names=last_names)


def test_given_an_invalid_name_when_creating_then_the_error_does_not_expose_it():
    last_names = "Martín Ruiz"

    with pytest.raises(InvalidPsychologistName) as error:
        PsychologistName(first_name="", last_names=last_names)

    assert last_names not in str(error.value)


@pytest.mark.parametrize(
    ("raw_first_name", "raw_last_names", "first_name", "last_names"),
    [
        ("Laura", "Martín Ruiz", "Laura", "Martín Ruiz"),
        ("  Laura ", " Martín Ruiz  ", "Laura", "Martín Ruiz"),
        ("María-José", "O'Brien", "María-José", "O'Brien"),
        ("Luis", "de la Fuente Martínez", "Luis", "de la Fuente Martínez"),
    ],
)
def test_given_a_valid_name_when_creating_then_it_only_strips_the_surrounding_spaces(
    raw_first_name, raw_last_names, first_name, last_names
):
    name = PsychologistName(first_name=raw_first_name, last_names=raw_last_names)

    assert name.first_name == first_name
    assert name.last_names == last_names
