import pytest
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId


@pytest.fixture
def patient_id() -> PatientId:
    return PatientId.generate()


@pytest.fixture
def patient_email() -> PatientEmail:
    return PatientEmail("ana@gmail.com")


@pytest.fixture
def registered_patient(patient_id: PatientId, patient_email: PatientEmail) -> Patient:
    return Patient.register(patient_id, patient_email)
