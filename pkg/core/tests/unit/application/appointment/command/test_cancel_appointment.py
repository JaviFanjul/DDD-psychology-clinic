import pytest
from core.application.appointment.command.cancel_appointment import CancelAppointmentCommand
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import AppointmentAlreadyCancelled, AppointmentNotFound
from core.domain.model.appointment.events import AppointmentCancelled


async def test_given_a_pending_appointment_when_handling_then_it_is_saved_cancelled(
    cancel_appointment_handler, appointment_repository, pending_appointment
):
    await cancel_appointment_handler.handle(command=CancelAppointmentCommand(id=pending_appointment.id))

    [appointment] = appointment_repository.saved
    assert appointment.id == pending_appointment.id
    assert appointment.status is AppointmentStatus.CANCELLED


async def test_given_a_pending_appointment_when_handling_then_appointment_cancelled_is_published(
    cancel_appointment_handler, event_bus, pending_appointment
):
    await cancel_appointment_handler.handle(command=CancelAppointmentCommand(id=pending_appointment.id))

    [event] = event_bus.published
    assert isinstance(event, AppointmentCancelled)
    assert event.appointment_id == pending_appointment.id


@pytest.mark.parametrize(
    ("appointment", "expected_error"),
    [("unknown", AppointmentNotFound), ("cancelled", AppointmentAlreadyCancelled)],
)
async def test_given_an_unchangeable_appointment_when_handling_then_it_raises_and_saves_nothing(
    cancel_appointment_handler,
    appointment_repository,
    event_bus,
    unit_of_work,
    cancelled_appointment,
    appointment,
    expected_error,
):
    ids = {"unknown": AppointmentId.generate(), "cancelled": cancelled_appointment.id}

    with pytest.raises(expected_error):
        await cancel_appointment_handler.handle(command=CancelAppointmentCommand(id=ids[appointment]))

    assert appointment_repository.saved == []
    assert event_bus.published == []
    assert not unit_of_work.committed


async def test_given_a_pending_appointment_when_handling_then_it_commits_before_publishing(
    cancel_appointment_handler, unit_of_work, pending_appointment
):
    await cancel_appointment_handler.handle(command=CancelAppointmentCommand(id=pending_appointment.id))

    assert unit_of_work.committed
    assert unit_of_work.published_before_commit == []
