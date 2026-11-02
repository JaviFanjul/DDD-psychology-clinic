from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractExchange
from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus
from core.infrastructure.rabbitmq.rabbitmq_event_serializer import RabbitMqEventSerializer

PATIENTS_EXCHANGE = "patients"


class RabbitMqEventBus(EventBus):
    def __init__(self, exchange: AbstractExchange) -> None:
        self._exchange = exchange

    async def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            routing_key, body = RabbitMqEventSerializer.to_message(event=event)
            await self._exchange.publish(
                message=Message(
                    body=body,
                    content_type="application/json",
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=routing_key,
            )
