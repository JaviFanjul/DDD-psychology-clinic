from patients.domain.model.patient.errors import InvalidPatientId


def test_given_a_malformed_value_when_creating_invalid_patient_id_then_its_message_names_it():
    malformed_value = "not-a-uuid"

    error = InvalidPatientId(malformed_value)

    assert str(error) == "'not-a-uuid' is not a valid UUID"
