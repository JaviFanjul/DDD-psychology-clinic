from aio_pika import DeliveryMode
from core.infrastructure.rabbitmq.rabbitmq_event_serializer import RabbitMqEventSerializer


async def test_given_patient_events_when_publishing_them_then_they_reach_the_exchange_in_order(
    event_bus, queue, events
):
    await event_bus.publish(events=events)

    messages = [await queue.get(timeout=5) for _ in events]
    assert [message.routing_key for message in messages] == [
        "patient.created",
        "patient.discharged",
        "patient.readmitted",
    ]
    assert all(message.content_type == "application/json" for message in messages)
    assert all(message.delivery_mode == DeliveryMode.PERSISTENT for message in messages)
    assert [
        RabbitMqEventSerializer.from_message(routing_key=message.routing_key, body=message.body) for message in messages
    ] == events
