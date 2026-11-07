import pytest
from core.domain.model.psychologist.errors import InvalidPsychologistPhone
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone

VALID_PHONE = {"prefix": "+34", "number": "687654321"}


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("prefix", ""),
        ("prefix", "   "),
        ("prefix", "+"),
        ("prefix", "+0"),
        ("prefix", "+1234"),
        ("prefix", "++34"),
        ("prefix", "0034"),
        ("prefix", "+3a"),
        ("prefix", "+٣٤"),
        ("number", ""),
        ("number", "   "),
        ("number", "123"),
        ("number", "123456789012345"),
        ("number", "68765432a"),
        ("number", "687/654/321"),
        ("number", "+687654321"),
        ("number", "٦٨٧٦٥٤٣٢١"),
    ],
)
def test_given_an_invalid_field_when_creating_then_it_raises_invalid_psychologist_phone(field, invalid_value):
    with pytest.raises(InvalidPsychologistPhone):
        PsychologistPhone(**{**VALID_PHONE, field: invalid_value})


def test_given_more_than_fifteen_digits_in_total_when_creating_then_it_raises_invalid_phone():
    with pytest.raises(InvalidPsychologistPhone):
        PsychologistPhone(prefix="+351", number="1234567890123")


def test_given_an_invalid_phone_when_creating_then_the_error_does_not_expose_it():
    number = "123"

    with pytest.raises(InvalidPsychologistPhone) as error:
        PsychologistPhone(prefix="+34", number=number)

    assert number not in str(error.value)


@pytest.mark.parametrize(
    ("raw_prefix", "raw_number", "expected_prefix", "expected_number"),
    [
        ("+34", "687654321", "+34", "687654321"),
        ("34", "687654321", "+34", "687654321"),
        (" +1 ", " (212) 555-0198 ", "+1", "2125550198"),
        ("+44", "20 7946 0958", "+44", "2079460958"),
        ("+351", "912.345.678", "+351", "912345678"),
    ],
)
def test_given_a_valid_phone_when_creating_then_it_holds_its_normalized_form(
    raw_prefix, raw_number, expected_prefix, expected_number
):
    phone = PsychologistPhone(prefix=raw_prefix, number=raw_number)

    assert (phone.prefix, phone.number) == (expected_prefix, expected_number)
