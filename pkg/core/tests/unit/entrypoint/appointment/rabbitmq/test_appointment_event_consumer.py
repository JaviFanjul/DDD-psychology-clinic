import pytest
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.errors import InvalidAppointmentId
from core.domain.model.appointment.events import (
    AppointmentCancelled,
    AppointmentCompleted,
    AppointmentModalityChanged,
    AppointmentRescheduled,
    AppointmentScheduled,
)


@pytest.mark.parametrize(
    ("routing_key", "expected_event"),
    [
        ("appointment.scheduled", AppointmentScheduled),
        ("appointment.rescheduled", AppointmentRescheduled),
        ("appointment.modality_changed", AppointmentModalityChanged),
        ("appointment.cancelled", AppointmentCancelled),
        ("appointment.completed", AppointmentCompleted),
    ],
)
async def test_given_an_appointment_event_when_consuming_then_its_handler_receives_it(
    consumer, handler, message, appointment_id, created_at, routing_key, expected_event
):
    await consumer.consume(message=message(routing_key=routing_key, appointment_id=appointment_id))

    assert handler.handled == [
        expected_event(appointment_id=AppointmentId.from_string(id=appointment_id), created_at=created_at)
    ]


async def test_given_a_malformed_appointment_id_when_consuming_then_it_raises_and_handles_nothing(
    consumer, handler, message
):
    with pytest.raises(InvalidAppointmentId):
        await consumer.consume(message=message(routing_key="appointment.scheduled", appointment_id="bad"))

    assert handler.handled == []
