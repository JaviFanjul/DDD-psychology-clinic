import pytest
from core.application.query.get_patient import GetPatientQuery
from core.domain.model.patient.errors import InvalidPatientId, PatientNotFound


def test_given_a_known_id_when_handling_then_it_returns_the_patient(
    handler, known_id, known_patient
):
    patient = handler.handle(GetPatientQuery(id=known_id))

    assert patient == known_patient


@pytest.mark.parametrize(
    ("id", "expected_error"),
    [
        ("0b6f4f3e-3f0a-4a51-9d7e-2f1c8a6b5d10", PatientNotFound),
        ("not-a-uuid", InvalidPatientId),
    ],
)
def test_given_an_id_without_a_patient_when_handling_then_it_raises(handler, id, expected_error):
    with pytest.raises(expected_error):
        handler.handle(GetPatientQuery(id=id))
