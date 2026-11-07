import pytest
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import AppointmentNotSaved
from core.domain.model.appointment.events import AppointmentCancelled
from core.domain.model.patient.events import PatientDischarged
from core.domain.model.patient.patient_id import PatientId


async def test_given_pending_appointments_when_the_patient_is_discharged_then_they_are_cancelled(
    cancel_pending_appointments_handler, appointment_repository, known_id, pending_appointments
):
    await cancel_pending_appointments_handler.handle(event=PatientDischarged(patient_id=known_id))

    assert appointment_repository.saved == pending_appointments
    assert all(appointment.status is AppointmentStatus.CANCELLED for appointment in appointment_repository.saved)


async def test_given_pending_appointments_when_the_patient_is_discharged_then_it_publishes_them(
    cancel_pending_appointments_handler, event_bus, known_id, pending_appointments
):
    await cancel_pending_appointments_handler.handle(event=PatientDischarged(patient_id=known_id))

    assert [type(event) for event in event_bus.published] == [AppointmentCancelled] * 2
    assert [event.appointment_id for event in event_bus.published] == [
        appointment.id for appointment in pending_appointments
    ]


async def test_given_no_pending_appointments_when_the_patient_is_discharged_then_nothing_changes(
    cancel_pending_appointments_handler, appointment_repository, event_bus
):
    await cancel_pending_appointments_handler.handle(event=PatientDischarged(patient_id=PatientId.generate()))

    assert appointment_repository.saved == []
    assert event_bus.published == []


async def test_given_pending_appointments_when_the_patient_is_discharged_then_it_commits_once_before_publishing(
    cancel_pending_appointments_handler, unit_of_work, known_id
):
    await cancel_pending_appointments_handler.handle(event=PatientDischarged(patient_id=known_id))

    assert unit_of_work.commits == 1
    assert unit_of_work.published_before_commit == []


async def test_given_a_save_that_fails_midway_when_the_patient_is_discharged_then_nothing_is_committed_nor_published(
    cancel_pending_appointments_handler_failing_on_second_save, unit_of_work, event_bus, known_id
):
    with pytest.raises(AppointmentNotSaved):
        await cancel_pending_appointments_handler_failing_on_second_save.handle(
            event=PatientDischarged(patient_id=known_id)
        )

    assert unit_of_work.commits == 0
    assert event_bus.published == []
