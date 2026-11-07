import pytest
from core.domain.model.patient.errors import InvalidPatientName
from core.domain.model.patient.patient_name import PatientName


@pytest.mark.parametrize(
    ("first_name", "last_names"),
    [
        ("", "García López"),
        ("   ", "García López"),
        ("Ana", ""),
        ("Ana", "   "),
    ],
)
def test_given_a_blank_part_when_creating_then_it_raises_invalid_patient_name(first_name, last_names):
    with pytest.raises(InvalidPatientName):
        PatientName(first_name=first_name, last_names=last_names)


def test_given_an_invalid_name_when_creating_then_the_error_does_not_expose_it():
    last_names = "García López"

    with pytest.raises(InvalidPatientName) as error:
        PatientName(first_name="", last_names=last_names)

    assert last_names not in str(error.value)


@pytest.mark.parametrize(
    ("raw_first_name", "raw_last_names", "first_name", "last_names"),
    [
        ("Ana", "García López", "Ana", "García López"),
        ("  Ana ", " García López  ", "Ana", "García López"),
        ("María-José", "O'Brien", "María-José", "O'Brien"),
        ("Luis", "de la Fuente Martínez", "Luis", "de la Fuente Martínez"),
    ],
)
def test_given_a_valid_name_when_creating_then_it_only_strips_the_surrounding_spaces(
    raw_first_name, raw_last_names, first_name, last_names
):
    name = PatientName(first_name=raw_first_name, last_names=raw_last_names)

    assert name.first_name == first_name
    assert name.last_names == last_names
