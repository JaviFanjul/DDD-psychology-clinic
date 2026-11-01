from core.domain.model.patient.events import PatientCreated
from core.domain.model.patient.patient import Patient


def test_given_an_id_and_an_email_when_creating_then_the_patient_holds_them(
    patient_id, patient_email
):
    patient = Patient.create(patient_id, patient_email)

    assert patient.id == patient_id
    assert patient.email == patient_email


def test_given_a_created_patient_when_pulling_then_it_returns_patient_created(
    created_patient, patient_id
):
    [event] = created_patient.pull_events()

    assert isinstance(event, PatientCreated)
    assert event.patient_id == patient_id


def test_given_events_already_pulled_when_pulling_again_then_it_returns_no_events(
    created_patient,
):
    created_patient.pull_events()

    events = created_patient.pull_events()

    assert events == []


def test_given_a_patient_built_with_the_constructor_when_pulling_then_it_returns_no_events(
    patient_id, patient_email
):
    patient = Patient(patient_id, patient_email)

    events = patient.pull_events()

    assert events == []
