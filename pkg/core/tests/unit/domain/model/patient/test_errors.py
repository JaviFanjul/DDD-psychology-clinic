from core.domain.model.patient.errors import InvalidPatientId, PatientNotFound


def test_given_a_malformed_value_when_creating_invalid_patient_id_then_its_message_names_it():
    malformed_value = "not-a-uuid"

    error = InvalidPatientId(value=malformed_value)

    assert str(error) == "'not-a-uuid' is not a valid UUID"


def test_given_an_id_when_creating_patient_not_found_then_its_message_names_it():
    id = "some-id"

    error = PatientNotFound(id=id)

    assert str(error) == "Patient 'some-id' was not found"
