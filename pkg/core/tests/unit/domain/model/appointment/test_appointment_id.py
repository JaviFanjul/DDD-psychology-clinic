from uuid import UUID

import pytest
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.errors import InvalidAppointmentId

A_UUID_STRING = "12345678-1234-4678-9234-567812345678"


def test_given_a_generated_id_when_generating_another_then_their_uuids_differ():
    first = AppointmentId.generate()

    second = AppointmentId.generate()

    assert first.id != second.id


def test_given_a_valid_string_when_parsing_then_it_holds_the_matching_uuid():
    valid_string = A_UUID_STRING

    appointment_id = AppointmentId.from_string(id=valid_string)

    assert appointment_id.id == UUID(valid_string)


def test_given_a_malformed_string_when_parsing_then_it_raises_invalid_appointment_id():
    malformed_string = "not-a-uuid"

    with pytest.raises(InvalidAppointmentId):
        AppointmentId.from_string(id=malformed_string)


def test_given_an_appointment_id_when_converting_to_string_then_it_returns_the_uuid_string():
    appointment_id = AppointmentId.from_string(id=A_UUID_STRING)

    string = str(appointment_id)

    assert string == A_UUID_STRING
