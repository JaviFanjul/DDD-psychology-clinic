import pytest
from core.application.appointment.command.reschedule_appointment import RescheduleAppointmentCommand
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.errors import (
    AppointmentAlreadyCancelled,
    AppointmentNotFound,
    AppointmentOverlaps,
)
from core.domain.model.appointment.events import AppointmentRescheduled


async def test_given_a_pending_appointment_and_a_free_agenda_when_handling_then_it_is_saved(
    reschedule_appointment_handler, appointment_repository, pending_appointment, other_slot
):
    await reschedule_appointment_handler.handle(
        command=RescheduleAppointmentCommand(id=pending_appointment.id, slot=other_slot)
    )

    [appointment] = appointment_repository.saved
    assert appointment.id == pending_appointment.id
    assert appointment.slot == other_slot


async def test_given_a_pending_appointment_and_a_free_agenda_when_handling_then_it_publishes_it(
    reschedule_appointment_handler, event_bus, pending_appointment, other_slot
):
    await reschedule_appointment_handler.handle(
        command=RescheduleAppointmentCommand(id=pending_appointment.id, slot=other_slot)
    )

    [event] = event_bus.published
    assert isinstance(event, AppointmentRescheduled)
    assert event.appointment_id == pending_appointment.id


async def test_given_a_pending_appointment_when_handling_then_it_checks_its_psychologist_agenda(
    reschedule_appointment_handler, free_agenda, pending_appointment, other_slot
):
    await reschedule_appointment_handler.handle(
        command=RescheduleAppointmentCommand(id=pending_appointment.id, slot=other_slot)
    )

    assert free_agenda.slot_queries == [
        (pending_appointment.psychologist_id, pending_appointment.id)
    ]


async def test_given_a_busy_agenda_when_handling_then_it_raises_and_saves_and_publishes_nothing(
    reschedule_appointment_handler_with_busy_agenda,
    appointment_repository,
    event_bus,
    pending_appointment,
    other_slot,
):
    with pytest.raises(AppointmentOverlaps):
        await reschedule_appointment_handler_with_busy_agenda.handle(
            command=RescheduleAppointmentCommand(id=pending_appointment.id, slot=other_slot)
        )

    assert appointment_repository.saved == []
    assert event_bus.published == []


async def test_given_an_unknown_id_when_handling_then_it_raises_and_saves_and_publishes_nothing(
    reschedule_appointment_handler, appointment_repository, event_bus, other_slot
):
    with pytest.raises(AppointmentNotFound):
        await reschedule_appointment_handler.handle(
            command=RescheduleAppointmentCommand(id=AppointmentId.generate(), slot=other_slot)
        )

    assert appointment_repository.saved == []
    assert event_bus.published == []


async def test_given_a_cancelled_appointment_when_handling_then_it_raises_before_checking_agenda(
    reschedule_appointment_handler,
    appointment_repository,
    event_bus,
    free_agenda,
    cancelled_appointment,
    other_slot,
):
    with pytest.raises(AppointmentAlreadyCancelled):
        await reschedule_appointment_handler.handle(
            command=RescheduleAppointmentCommand(id=cancelled_appointment.id, slot=other_slot)
        )

    assert free_agenda.slot_queries == []
    assert appointment_repository.saved == []
    assert event_bus.published == []
