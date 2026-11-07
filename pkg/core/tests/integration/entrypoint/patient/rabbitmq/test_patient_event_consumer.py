from core.domain.model.patient.events import PatientCreated, PatientDischarged, PatientReadmitted


async def test_given_patient_events_published_by_core_when_consuming_then_its_handler_receives_them(
    consume, event_bus, wait_until, patient_id, handler
):
    await consume(handler=handler)
    events = [
        PatientCreated(patient_id=patient_id),
        PatientDischarged(patient_id=patient_id),
        PatientReadmitted(patient_id=patient_id),
    ]

    await event_bus.publish(events=events)
    await wait_until(condition=lambda: len(handler.handled) == 3)

    assert handler.handled == events


async def test_given_a_handler_that_fails_when_consuming_then_the_event_is_delivered_again(
    consume, event_bus, wait_until, patient_id, failing_once_handler
):
    handler = failing_once_handler
    await consume(handler=handler)
    event = PatientDischarged(patient_id=patient_id)

    await event_bus.publish(events=[event])
    await wait_until(condition=lambda: len(handler.handled) == 2)

    assert handler.handled == [event, event]
