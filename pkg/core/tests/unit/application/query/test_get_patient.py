import pytest
from core.application.query.get_patient import GetPatientQuery
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.patient_id import PatientId


def test_given_a_known_id_when_handling_then_it_returns_the_patient(
    handler, known_id, known_patient
):
    patient = handler.handle(query=GetPatientQuery(id=PatientId.from_string(id=known_id)))

    assert patient == known_patient


def test_given_an_id_without_a_patient_when_handling_then_it_raises_patient_not_found(handler):
    with pytest.raises(PatientNotFound):
        handler.handle(query=GetPatientQuery(id=PatientId.generate()))
