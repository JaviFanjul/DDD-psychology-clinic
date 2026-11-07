import pytest
from core.domain.model.patient.errors import PatientAlreadyActive, PatientAlreadyDischarged
from core.domain.model.patient.events import (
    PatientCreated,
    PatientDischarged,
    PatientReadmitted,
)
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_status import PatientStatus


def test_given_its_data_when_creating_then_the_patient_holds_it(
    patient_id, patient_email, patient_name, patient_phone, patient_address
):
    patient = Patient.create(
        id=patient_id,
        email=patient_email,
        name=patient_name,
        phone=patient_phone,
        address=patient_address,
    )

    assert patient.id == patient_id
    assert patient.email == patient_email
    assert patient.name == patient_name
    assert patient.phone == patient_phone
    assert patient.address == patient_address
    assert patient.status is PatientStatus.ACTIVE


def test_given_a_created_patient_when_pulling_then_it_returns_patient_created(created_patient, patient_id):
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
    patient_id, patient_email, patient_name, patient_phone, patient_address
):
    patient = Patient(
        id=patient_id,
        email=patient_email,
        name=patient_name,
        phone=patient_phone,
        address=patient_address,
        status=PatientStatus.ACTIVE,
    )

    events = patient.pull_events()

    assert events == []


def test_given_an_active_patient_when_discharging_then_it_is_discharged(created_patient):
    created_patient.discharge()

    assert created_patient.status is PatientStatus.DISCHARGED


def test_given_an_active_patient_when_discharging_then_it_records_patient_discharged(created_patient, patient_id):
    created_patient.pull_events()

    created_patient.discharge()

    [event] = created_patient.pull_events()
    assert isinstance(event, PatientDischarged)
    assert event.patient_id == patient_id


def test_given_a_discharged_patient_when_discharging_again_then_it_raises_and_records_nothing(
    created_patient,
):
    created_patient.discharge()
    created_patient.pull_events()

    with pytest.raises(PatientAlreadyDischarged):
        created_patient.discharge()

    assert created_patient.pull_events() == []


def test_given_a_discharged_patient_when_readmitting_then_it_is_active(created_patient):
    created_patient.discharge()

    created_patient.readmit()

    assert created_patient.status is PatientStatus.ACTIVE


def test_given_a_discharged_patient_when_readmitting_then_it_records_patient_readmitted(created_patient, patient_id):
    created_patient.discharge()
    created_patient.pull_events()

    created_patient.readmit()

    [event] = created_patient.pull_events()
    assert isinstance(event, PatientReadmitted)
    assert event.patient_id == patient_id


def test_given_an_active_patient_when_readmitting_then_it_raises_and_records_nothing(
    created_patient,
):
    created_patient.pull_events()

    with pytest.raises(PatientAlreadyActive):
        created_patient.readmit()

    assert created_patient.pull_events() == []


def test_given_two_patients_with_the_same_id_when_comparing_then_they_are_equal(
    created_patient, patient_id, patient_name, patient_phone, patient_address
):
    same_patient = Patient(
        id=patient_id,
        email=PatientEmail(value="ana.garcia@gmail.com"),
        name=patient_name,
        phone=patient_phone,
        address=patient_address,
        status=PatientStatus.DISCHARGED,
    )

    assert same_patient == created_patient
    assert hash(same_patient) == hash(created_patient)


def test_given_two_patients_with_different_ids_when_comparing_then_they_are_not_equal(
    created_patient, patient_email, patient_name, patient_phone, patient_address
):
    other_patient = Patient(
        id=PatientId.generate(),
        email=patient_email,
        name=patient_name,
        phone=patient_phone,
        address=patient_address,
        status=PatientStatus.ACTIVE,
    )

    assert other_patient != created_patient
