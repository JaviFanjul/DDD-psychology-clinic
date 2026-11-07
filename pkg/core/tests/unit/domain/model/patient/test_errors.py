import pytest
from core.domain.model.patient.errors import (
    InvalidPatientId,
    PatientAlreadyActive,
    PatientAlreadyDischarged,
    PatientNotActive,
    PatientNotFound,
    PatientNotLoaded,
    PatientNotNotified,
    PatientNotSaved,
)


def test_given_a_malformed_value_when_creating_invalid_patient_id_then_its_message_names_it():
    malformed_value = "not-a-uuid"

    error = InvalidPatientId(value=malformed_value)

    assert str(error) == "'not-a-uuid' is not a valid UUID"


def test_given_an_id_when_creating_patient_not_found_then_its_message_names_it():
    id = "some-id"

    error = PatientNotFound(id=id)

    assert str(error) == "Patient 'some-id' was not found"


@pytest.mark.parametrize(
    ("error_type", "expected_message"),
    [
        (PatientAlreadyDischarged, "Patient 'some-id' is already discharged"),
        (PatientAlreadyActive, "Patient 'some-id' is already active"),
        (PatientNotActive, "Patient 'some-id' is not active"),
    ],
)
def test_given_an_id_when_creating_a_status_error_then_its_message_names_it(
    error_type, expected_message
):
    id = "some-id"

    error = error_type(id=id)

    assert str(error) == expected_message


@pytest.mark.parametrize(
    ("error_type", "expected_message"),
    [
        (PatientNotSaved, "Patient 'some-id' could not be saved"),
        (PatientNotLoaded, "Patient 'some-id' could not be loaded"),
        (PatientNotNotified, "Patient 'some-id' could not be notified"),
    ],
)
def test_given_an_id_when_creating_an_infrastructure_error_then_its_message_names_it(
    error_type, expected_message
):
    id = "some-id"

    error = error_type(id=id)

    assert str(error) == expected_message
