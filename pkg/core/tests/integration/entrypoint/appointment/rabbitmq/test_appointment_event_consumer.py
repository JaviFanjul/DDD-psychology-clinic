from core.domain.model.appointment.events import (
    AppointmentCancelled,
    AppointmentCompleted,
    AppointmentModalityChanged,
    AppointmentRescheduled,
    AppointmentScheduled,
)


async def test_given_appointment_events_published_by_core_when_consuming_then_its_handler_receives_them(
    consume, event_bus, wait_until, appointment_id, handler
):
    await consume(handler=handler)
    events = [
        AppointmentScheduled(appointment_id=appointment_id),
        AppointmentRescheduled(appointment_id=appointment_id),
        AppointmentModalityChanged(appointment_id=appointment_id),
        AppointmentCancelled(appointment_id=appointment_id),
        AppointmentCompleted(appointment_id=appointment_id),
    ]

    await event_bus.publish(events=events)
    await wait_until(condition=lambda: len(handler.handled) == 5)

    assert handler.handled == events


async def test_given_a_handler_that_fails_when_consuming_then_the_event_is_delivered_again(
    consume, event_bus, wait_until, appointment_id, failing_once_handler
):
    handler = failing_once_handler
    await consume(handler=handler)
    event = AppointmentCancelled(appointment_id=appointment_id)

    await event_bus.publish(events=[event])
    await wait_until(condition=lambda: len(handler.handled) == 2)

    assert handler.handled == [event, event]
