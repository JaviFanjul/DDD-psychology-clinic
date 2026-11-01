from patients.domain.model.patient.events import PatientRegistered
from patients.domain.model.patient.patient import Patient
from patients.domain.model.patient.patient_id import PatientId


def test_given_an_id_when_registering_then_the_patient_holds_that_id():
    patient_id = PatientId.generate()

    patient = Patient.register(patient_id)

    assert patient.id == patient_id


def test_given_a_registered_patient_when_pulling_then_it_returns_patient_registered():
    patient_id = PatientId.generate()
    patient = Patient.register(patient_id)

    [event] = patient.pull_events()

    assert isinstance(event, PatientRegistered)
    assert event.patient_id == patient_id


def test_given_events_already_pulled_when_pulling_again_then_it_returns_no_events():
    patient = Patient.register(PatientId.generate())
    patient.pull_events()

    events = patient.pull_events()

    assert events == []


def test_given_a_patient_built_with_the_constructor_when_pulling_then_it_returns_no_events():
    patient = Patient(PatientId.generate())

    events = patient.pull_events()

    assert events == []
