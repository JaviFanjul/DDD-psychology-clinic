import pytest
from core.domain.model.psychologist.errors import InvalidPsychologistEmail
from core.domain.model.psychologist.psychologist_email import PsychologistEmail


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",
        "laura",
        "laura@",
        "@clinica.es",
        "laura@clinica",
        "laura@@clinica.es",
        "laura@clinica..es",
        "laura martin@clinica.es",
    ],
)
def test_given_an_invalid_value_when_creating_then_it_raises_invalid_psychologist_email(
    invalid_email,
):
    with pytest.raises(InvalidPsychologistEmail):
        PsychologistEmail(value=invalid_email)


def test_given_an_invalid_email_when_creating_then_the_error_does_not_expose_it():
    invalid_email = "laura.martin@clinica"

    with pytest.raises(InvalidPsychologistEmail) as error:
        PsychologistEmail(value=invalid_email)

    assert invalid_email not in str(error.value)


@pytest.mark.parametrize(
    ("raw_email", "expected"),
    [
        ("laura.martin@clinica.co.uk", "laura.martin@clinica.co.uk"),
        ("Laura@Clinica.es", "laura@clinica.es"),
        ("  laura@clinica.es ", "laura@clinica.es"),
    ],
)
def test_given_a_valid_email_when_creating_then_it_holds_its_normalized_form(raw_email, expected):
    email = PsychologistEmail(value=raw_email)

    assert email.value == expected
