import pytest
from core.application.appointment.command.change_appointment_modality import (
    ChangeAppointmentModalityCommand,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.errors import AppointmentAlreadyCancelled, AppointmentNotFound
from core.domain.model.appointment.events import AppointmentModalityChanged


async def test_given_a_pending_appointment_when_handling_then_it_is_saved_with_the_new_modality(
    change_appointment_modality_handler, appointment_repository, pending_appointment
):
    await change_appointment_modality_handler.handle(
        command=ChangeAppointmentModalityCommand(id=pending_appointment.id, modality=AppointmentModality.ONLINE)
    )

    [appointment] = appointment_repository.saved
    assert appointment.id == pending_appointment.id
    assert appointment.modality is AppointmentModality.ONLINE


async def test_given_a_pending_appointment_when_handling_then_modality_changed_is_published(
    change_appointment_modality_handler, event_bus, pending_appointment
):
    await change_appointment_modality_handler.handle(
        command=ChangeAppointmentModalityCommand(id=pending_appointment.id, modality=AppointmentModality.ONLINE)
    )

    [event] = event_bus.published
    assert isinstance(event, AppointmentModalityChanged)
    assert event.appointment_id == pending_appointment.id


@pytest.mark.parametrize(
    ("appointment", "expected_error"),
    [("unknown", AppointmentNotFound), ("cancelled", AppointmentAlreadyCancelled)],
)
async def test_given_an_unchangeable_appointment_when_handling_then_it_raises_and_saves_nothing(
    change_appointment_modality_handler,
    appointment_repository,
    event_bus,
    cancelled_appointment,
    appointment,
    expected_error,
):
    ids = {"unknown": AppointmentId.generate(), "cancelled": cancelled_appointment.id}

    with pytest.raises(expected_error):
        await change_appointment_modality_handler.handle(
            command=ChangeAppointmentModalityCommand(id=ids[appointment], modality=AppointmentModality.ONLINE)
        )

    assert appointment_repository.saved == []
    assert event_bus.published == []
