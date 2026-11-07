import pytest
from core.application.appointment.command.complete_appointment import CompleteAppointmentCommand
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import AppointmentAlreadyCancelled, AppointmentNotFound
from core.domain.model.appointment.events import AppointmentCompleted


async def test_given_a_pending_appointment_when_handling_then_it_is_saved_completed(
    complete_appointment_handler, appointment_repository, pending_appointment
):
    await complete_appointment_handler.handle(command=CompleteAppointmentCommand(id=pending_appointment.id))

    [appointment] = appointment_repository.saved
    assert appointment.id == pending_appointment.id
    assert appointment.status is AppointmentStatus.COMPLETED


async def test_given_a_pending_appointment_when_handling_then_appointment_completed_is_published(
    complete_appointment_handler, event_bus, pending_appointment
):
    await complete_appointment_handler.handle(command=CompleteAppointmentCommand(id=pending_appointment.id))

    [event] = event_bus.published
    assert isinstance(event, AppointmentCompleted)
    assert event.appointment_id == pending_appointment.id


@pytest.mark.parametrize(
    ("appointment", "expected_error"),
    [("unknown", AppointmentNotFound), ("cancelled", AppointmentAlreadyCancelled)],
)
async def test_given_an_unchangeable_appointment_when_handling_then_it_raises_and_saves_nothing(
    complete_appointment_handler,
    appointment_repository,
    event_bus,
    cancelled_appointment,
    appointment,
    expected_error,
):
    ids = {"unknown": AppointmentId.generate(), "cancelled": cancelled_appointment.id}

    with pytest.raises(expected_error):
        await complete_appointment_handler.handle(command=CompleteAppointmentCommand(id=ids[appointment]))

    assert appointment_repository.saved == []
    assert event_bus.published == []
