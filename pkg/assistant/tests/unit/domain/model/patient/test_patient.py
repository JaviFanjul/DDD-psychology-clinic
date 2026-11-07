import pytest
from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_id import PatientId


def test_given_an_id_when_creating_then_the_patient_holds_it_and_is_active(patient_id):
    patient = Patient.create(id=patient_id)

    assert patient.id == patient_id
    assert patient.is_active


@pytest.mark.parametrize("times", [1, 2])
def test_given_an_active_patient_when_deactivating_then_it_is_not_active(created_patient, times):
    for _ in range(times):
        created_patient.deactivate()

    assert not created_patient.is_active


@pytest.mark.parametrize("times", [1, 2])
def test_given_an_inactive_patient_when_activating_then_it_is_active(created_patient, times):
    created_patient.deactivate()

    for _ in range(times):
        created_patient.activate()

    assert created_patient.is_active


def test_given_two_patients_with_the_same_id_when_comparing_then_they_are_equal(created_patient, patient_id):
    same_patient = Patient(id=patient_id, active=False)

    assert same_patient == created_patient
    assert hash(same_patient) == hash(created_patient)


def test_given_two_patients_with_different_ids_when_comparing_then_they_are_not_equal(
    created_patient,
):
    other_patient = Patient.create(id=PatientId.from_string(id="12345678-1234-4678-9234-567812345678"))

    assert other_patient != created_patient
