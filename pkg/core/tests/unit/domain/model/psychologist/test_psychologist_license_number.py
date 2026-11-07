import pytest
from core.domain.model.psychologist.errors import InvalidPsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber


@pytest.mark.parametrize(
    "invalid_license_number",
    [
        "",
        "   ",
        "12345",
        "M-",
        "M-123",
        "M-1234567",
        "ABC-12345",
        "M--12345",
        "M 12345",
        "M-1234A",
        "Ñ-12345",
        "M-١٢٣٤٥",
    ],
)
def test_given_an_invalid_value_when_creating_then_it_raises_invalid_license_number(
    invalid_license_number,
):
    with pytest.raises(InvalidPsychologistLicenseNumber):
        PsychologistLicenseNumber(value=invalid_license_number)


def test_given_an_invalid_license_number_when_creating_then_the_error_does_not_expose_it():
    invalid_license_number = "M-123"

    with pytest.raises(InvalidPsychologistLicenseNumber) as error:
        PsychologistLicenseNumber(value=invalid_license_number)

    assert invalid_license_number not in str(error.value)


@pytest.mark.parametrize(
    ("raw_license_number", "expected"),
    [
        ("M-12345", "M-12345"),
        ("m-12345", "M-12345"),
        ("M12345", "M-12345"),
        ("  CV-0123 ", "CV-0123"),
        ("cv123456", "CV-123456"),
    ],
)
def test_given_a_valid_license_number_when_creating_then_it_holds_its_normalized_form(raw_license_number, expected):
    license_number = PsychologistLicenseNumber(value=raw_license_number)

    assert license_number.value == expected
