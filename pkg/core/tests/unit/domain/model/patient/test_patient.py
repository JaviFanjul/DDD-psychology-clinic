from core.domain.model.patient.events import PatientRegistered
from core.domain.model.patient.patient import Patient


def test_given_an_id_and_an_email_when_registering_then_the_patient_holds_them(
    patient_id, patient_email
):
    patient = Patient.register(patient_id, patient_email)

    assert patient.id == patient_id
    assert patient.email == patient_email


def test_given_a_registered_patient_when_pulling_then_it_returns_patient_registered(
    registered_patient, patient_id
):
    [event] = registered_patient.pull_events()

    assert isinstance(event, PatientRegistered)
    assert event.patient_id == patient_id


def test_given_events_already_pulled_when_pulling_again_then_it_returns_no_events(
    registered_patient,
):
    registered_patient.pull_events()

    events = registered_patient.pull_events()

    assert events == []


def test_given_a_patient_built_with_the_constructor_when_pulling_then_it_returns_no_events(
    patient_id, patient_email
):
    patient = Patient(patient_id, patient_email)

    events = patient.pull_events()

    assert events == []
