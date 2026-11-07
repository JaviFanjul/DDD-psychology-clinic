import pytest
from core.domain.model.patient.errors import InvalidPatientAddress
from core.domain.model.patient.patient_address import PatientAddress

VALID_ADDRESS = {
    "street": "Calle Mayor 3, 2º B",
    "postal_code": "08001",
    "city": "Barcelona",
    "province": "Barcelona",
}


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("street", ""),
        ("street", "   "),
        ("city", ""),
        ("city", "   "),
        ("province", ""),
        ("province", "   "),
        ("postal_code", ""),
        ("postal_code", "   "),
        ("postal_code", "0800"),
        ("postal_code", "080011"),
        ("postal_code", "0800A"),
        ("postal_code", "08 01"),
        ("postal_code", "٠٨٠٠١"),
    ],
)
def test_given_an_invalid_field_when_creating_then_it_raises_invalid_patient_address(field, invalid_value):
    with pytest.raises(InvalidPatientAddress):
        PatientAddress(**{**VALID_ADDRESS, field: invalid_value})


def test_given_an_invalid_address_when_creating_then_the_error_does_not_expose_it():
    street = "Calle Mayor 3, 2º B"

    with pytest.raises(InvalidPatientAddress) as error:
        PatientAddress(**{**VALID_ADDRESS, "street": street, "postal_code": "0800"})

    assert street not in str(error.value)


def test_given_a_valid_address_when_creating_then_it_strips_the_surrounding_spaces():
    address = PatientAddress(
        street="  Calle Mayor 3, 2º B ",
        postal_code=" 08001 ",
        city=" Barcelona  ",
        province="  Barcelona ",
    )

    assert address == PatientAddress(**VALID_ADDRESS)
    assert address.street == "Calle Mayor 3, 2º B"
    assert address.postal_code == "08001"
    assert address.city == "Barcelona"
    assert address.province == "Barcelona"
