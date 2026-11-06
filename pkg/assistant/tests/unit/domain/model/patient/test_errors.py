import pytest
from assistant.domain.model.patient.errors import (
    InvalidPatientId,
    PatientNotActive,
    PatientNotFound,
    PatientNotLoaded,
    PatientNotSaved,
)


def test_given_a_malformed_value_when_creating_invalid_patient_id_then_its_message_names_it():
    malformed_value = "not-a-uuid"

    error = InvalidPatientId(value=malformed_value)

    assert str(error) == "'not-a-uuid' is not a valid UUID"


@pytest.mark.parametrize(
    ("error_type", "expected_message"),
    [
        (PatientNotFound, "Patient 'some-id' was not found"),
        (PatientNotActive, "Patient 'some-id' is not active"),
        (PatientNotSaved, "Patient 'some-id' could not be saved"),
        (PatientNotLoaded, "Patient 'some-id' could not be loaded"),
    ],
)
def test_given_an_id_when_creating_a_patient_error_then_its_message_names_it(
    error_type, expected_message
):
    id = "some-id"

    error = error_type(id=id)

    assert str(error) == expected_message
