import pytest
from core.domain.model.appointment.errors import (
    AppointmentAlreadyCancelled,
    AppointmentAlreadyCompleted,
    AppointmentNotFound,
    AppointmentNotLoaded,
    AppointmentNotSaved,
    AppointmentOverlaps,
    InvalidAppointmentId,
    InvalidAppointmentModality,
    PatientAppointmentsNotLoaded,
    PsychologistAppointmentsNotLoaded,
)


@pytest.mark.parametrize(
    ("error_type", "expected_message"),
    [
        (InvalidAppointmentId, "'some-value' is not a valid UUID"),
        (InvalidAppointmentModality, "'some-value' is not a valid appointment modality"),
    ],
)
def test_given_a_value_when_creating_an_invalid_value_error_then_its_message_names_it(error_type, expected_message):
    value = "some-value"

    error = error_type(value=value)

    assert str(error) == expected_message


@pytest.mark.parametrize(
    ("error_type", "expected_message"),
    [
        (AppointmentNotFound, "Appointment 'some-id' was not found"),
        (AppointmentNotSaved, "Appointment 'some-id' could not be saved"),
        (AppointmentNotLoaded, "Appointment 'some-id' could not be loaded"),
        (AppointmentAlreadyCancelled, "Appointment 'some-id' is already cancelled"),
        (AppointmentAlreadyCompleted, "Appointment 'some-id' is already completed"),
    ],
)
def test_given_an_id_when_creating_an_error_then_its_message_names_it(error_type, expected_message):
    id = "some-id"

    error = error_type(id=id)

    assert str(error) == expected_message


def test_given_a_psychologist_id_when_creating_appointment_overlaps_then_its_message_names_it():
    psychologist_id = "some-id"

    error = AppointmentOverlaps(psychologist_id=psychologist_id)

    assert str(error) == ("Psychologist 'some-id' already has a pending appointment at that time")


def test_given_a_patient_id_when_creating_appointments_not_loaded_then_its_message_names_it():
    patient_id = "some-id"

    error = PatientAppointmentsNotLoaded(patient_id=patient_id)

    assert str(error) == "Appointments of patient 'some-id' could not be loaded"


def test_given_a_psychologist_id_when_creating_its_appointments_not_loaded_then_it_names_it():
    psychologist_id = "some-id"

    error = PsychologistAppointmentsNotLoaded(psychologist_id=psychologist_id)

    assert str(error) == "Appointments of psychologist 'some-id' could not be loaded"
