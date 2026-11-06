import pytest
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_id import PatientId


@pytest.fixture
def patient_id() -> PatientId:
    return PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7")


@pytest.fixture
def created_patient(patient_id: PatientId) -> Patient:
    return Patient.create(id=patient_id)
