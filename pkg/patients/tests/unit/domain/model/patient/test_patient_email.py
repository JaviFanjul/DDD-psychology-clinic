import pytest
from patients.domain.model.patient.errors import InvalidPatientEmail
from patients.domain.model.patient.patient_email import PatientEmail


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",
        "ana",
        "ana@",
        "@gmail.com",
        "ana@gmail",
        "ana@@gmail.com",
        "ana@gmail..com",
        "ana garcia@gmail.com",
    ],
)
def test_given_an_invalid_value_when_creating_then_it_raises_invalid_patient_email(invalid_email):
    with pytest.raises(InvalidPatientEmail):
        PatientEmail(invalid_email)


def test_given_an_invalid_email_when_creating_then_the_error_does_not_expose_it():
    invalid_email = "ana.garcia@gmail"

    with pytest.raises(InvalidPatientEmail) as error:
        PatientEmail(invalid_email)

    assert invalid_email not in str(error.value)


@pytest.mark.parametrize(
    ("raw_email", "expected"),
    [
        ("ana.garcia@clinica.co.uk", "ana.garcia@clinica.co.uk"),
        ("Ana@Gmail.com", "ana@gmail.com"),
        ("  ana@gmail.com ", "ana@gmail.com"),
    ],
)
def test_given_a_valid_email_when_creating_then_it_holds_its_normalized_form(raw_email, expected):
    email = PatientEmail(raw_email)

    assert email.value == expected
