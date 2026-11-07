import json
from datetime import datetime
from typing import Any

from aio_pika.abc import AbstractIncomingMessage
from core.domain.event_bus import EventHandler
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.events import (
    AppointmentCancelled,
    AppointmentCompleted,
    AppointmentModalityChanged,
    AppointmentRescheduled,
    AppointmentScheduled,
)

CORE_EXCHANGE = "core"
EVENT_BY_ROUTING_KEY: dict[
    str,
    type[
        AppointmentScheduled
        | AppointmentRescheduled
        | AppointmentModalityChanged
        | AppointmentCancelled
        | AppointmentCompleted
    ],
] = {
    "appointment.scheduled": AppointmentScheduled,
    "appointment.rescheduled": AppointmentRescheduled,
    "appointment.modality_changed": AppointmentModalityChanged,
    "appointment.cancelled": AppointmentCancelled,
    "appointment.completed": AppointmentCompleted,
}


class AppointmentEventConsumer:
    def __init__(self, handler: EventHandler[Any]) -> None:
        self._handler = handler

    async def consume(self, message: AbstractIncomingMessage) -> None:
        async with message.process(requeue=True):
            body: dict[str, str] = json.loads(message.body)
            event_type = EVENT_BY_ROUTING_KEY[str(message.routing_key)]
            event = event_type(
                appointment_id=AppointmentId.from_string(id=body["appointment_id"]),
                created_at=datetime.fromisoformat(body["created_at"]),
            )
            await self._handler.handle(event=event)
