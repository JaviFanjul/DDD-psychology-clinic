import pytest
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.errors import InvalidAppointmentModality


@pytest.mark.parametrize(
    ("value", "expected_modality"),
    [("in_person", AppointmentModality.IN_PERSON), ("online", AppointmentModality.ONLINE)],
)
def test_given_a_known_value_when_parsing_then_it_returns_its_modality(value, expected_modality):
    modality = AppointmentModality.from_string(value=value)

    assert modality is expected_modality


@pytest.mark.parametrize("value", ["", "phone", "ONLINE"])
def test_given_an_unknown_value_when_parsing_then_it_raises_invalid_appointment_modality(value):
    with pytest.raises(InvalidAppointmentModality):
        AppointmentModality.from_string(value=value)
