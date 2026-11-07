import pytest
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import (
    AppointmentAlreadyCancelled,
    AppointmentAlreadyCompleted,
)
from core.domain.model.appointment.events import (
    AppointmentCancelled,
    AppointmentCompleted,
    AppointmentModalityChanged,
    AppointmentRescheduled,
    AppointmentScheduled,
)


def test_given_its_data_when_scheduling_then_the_appointment_is_pending_and_holds_it(
    appointment_id, patient_id, psychologist_id, slot
):
    appointment = Appointment.schedule(
        id=appointment_id,
        patient_id=patient_id,
        psychologist_id=psychologist_id,
        slot=slot,
        modality=AppointmentModality.ONLINE,
    )

    assert appointment.id == appointment_id
    assert appointment.patient_id == patient_id
    assert appointment.psychologist_id == psychologist_id
    assert appointment.slot == slot
    assert appointment.modality is AppointmentModality.ONLINE
    assert appointment.status is AppointmentStatus.PENDING


def test_given_a_scheduled_appointment_when_pulling_then_it_returns_appointment_scheduled(
    scheduled_appointment, appointment_id
):
    [event] = scheduled_appointment.pull_events()

    assert isinstance(event, AppointmentScheduled)
    assert event.appointment_id == appointment_id


def test_given_events_already_pulled_when_pulling_again_then_it_returns_no_events(
    scheduled_appointment,
):
    scheduled_appointment.pull_events()

    events = scheduled_appointment.pull_events()

    assert events == []


def test_given_an_appointment_built_with_the_constructor_when_pulling_then_it_returns_no_events(
    appointment_id, patient_id, psychologist_id, slot
):
    appointment = Appointment(
        id=appointment_id,
        patient_id=patient_id,
        psychologist_id=psychologist_id,
        slot=slot,
        modality=AppointmentModality.IN_PERSON,
        status=AppointmentStatus.PENDING,
    )

    events = appointment.pull_events()

    assert events == []


def test_given_a_pending_appointment_when_rescheduling_then_it_holds_the_new_slot_and_records_it(
    scheduled_appointment, appointment_id, other_slot
):
    scheduled_appointment.pull_events()

    scheduled_appointment.reschedule(slot=other_slot)

    assert scheduled_appointment.slot == other_slot
    [event] = scheduled_appointment.pull_events()
    assert isinstance(event, AppointmentRescheduled)
    assert event.appointment_id == appointment_id


def test_given_a_pending_appointment_when_rescheduling_to_its_slot_then_it_records_nothing(
    scheduled_appointment, slot
):
    scheduled_appointment.pull_events()

    scheduled_appointment.reschedule(slot=slot)

    assert scheduled_appointment.pull_events() == []


def test_given_a_pending_appointment_when_changing_its_modality_then_it_holds_it_and_records_it(
    scheduled_appointment, appointment_id
):
    scheduled_appointment.pull_events()

    scheduled_appointment.change_modality(modality=AppointmentModality.ONLINE)

    assert scheduled_appointment.modality is AppointmentModality.ONLINE
    [event] = scheduled_appointment.pull_events()
    assert isinstance(event, AppointmentModalityChanged)
    assert event.appointment_id == appointment_id


def test_given_a_pending_appointment_when_changing_to_its_modality_then_it_records_nothing(
    scheduled_appointment,
):
    scheduled_appointment.pull_events()

    scheduled_appointment.change_modality(modality=AppointmentModality.IN_PERSON)

    assert scheduled_appointment.pull_events() == []


@pytest.mark.parametrize(
    ("transition", "expected_status", "expected_event"),
    [
        ("cancel", AppointmentStatus.CANCELLED, AppointmentCancelled),
        ("complete", AppointmentStatus.COMPLETED, AppointmentCompleted),
    ],
)
def test_given_a_pending_appointment_when_closing_it_then_it_changes_status_and_records_it(
    scheduled_appointment, appointment_id, transition, expected_status, expected_event
):
    scheduled_appointment.pull_events()

    getattr(scheduled_appointment, transition)()

    assert scheduled_appointment.status is expected_status
    [event] = scheduled_appointment.pull_events()
    assert isinstance(event, expected_event)
    assert event.appointment_id == appointment_id


@pytest.mark.parametrize(
    ("closing", "expected_error"),
    [("cancel", AppointmentAlreadyCancelled), ("complete", AppointmentAlreadyCompleted)],
)
@pytest.mark.parametrize(
    "change",
    [
        lambda appointment, other_slot: appointment.reschedule(slot=other_slot),
        lambda appointment, other_slot: appointment.change_modality(
            modality=AppointmentModality.ONLINE
        ),
        lambda appointment, other_slot: appointment.cancel(),
        lambda appointment, other_slot: appointment.complete(),
    ],
    ids=["reschedule", "change_modality", "cancel", "complete"],
)
def test_given_a_closed_appointment_when_changing_it_then_it_raises_and_records_nothing(
    scheduled_appointment, other_slot, closing, expected_error, change
):
    getattr(scheduled_appointment, closing)()
    scheduled_appointment.pull_events()

    with pytest.raises(expected_error):
        change(scheduled_appointment, other_slot)

    assert scheduled_appointment.pull_events() == []


def test_given_two_appointments_with_the_same_id_when_comparing_then_they_are_equal(
    scheduled_appointment, appointment_id, patient_id, psychologist_id, other_slot
):
    same_appointment = Appointment(
        id=appointment_id,
        patient_id=patient_id,
        psychologist_id=psychologist_id,
        slot=other_slot,
        modality=AppointmentModality.ONLINE,
        status=AppointmentStatus.CANCELLED,
    )

    assert same_appointment == scheduled_appointment
    assert hash(same_appointment) == hash(scheduled_appointment)


def test_given_two_appointments_with_different_ids_when_comparing_then_they_are_not_equal(
    scheduled_appointment, patient_id, psychologist_id, slot
):
    other_appointment = Appointment(
        id=AppointmentId.generate(),
        patient_id=patient_id,
        psychologist_id=psychologist_id,
        slot=slot,
        modality=AppointmentModality.IN_PERSON,
        status=AppointmentStatus.PENDING,
    )

    assert other_appointment != scheduled_appointment
