import json
from datetime import datetime
from typing import Any

from aio_pika.abc import AbstractIncomingMessage
from core.domain.event_bus import EventHandler
from core.domain.model.patient.events import PatientCreated, PatientDischarged, PatientReadmitted
from core.domain.model.patient.patient_id import PatientId

CORE_EXCHANGE = "core"
EVENT_BY_ROUTING_KEY: dict[str, type[PatientCreated | PatientDischarged | PatientReadmitted]] = {
    "patient.created": PatientCreated,
    "patient.discharged": PatientDischarged,
    "patient.readmitted": PatientReadmitted,
}


class PatientEventConsumer:
    def __init__(self, handler: EventHandler[Any]) -> None:
        self._handler = handler

    async def consume(self, message: AbstractIncomingMessage) -> None:
        async with message.process(requeue=True):
            body: dict[str, str] = json.loads(message.body)
            event_type = EVENT_BY_ROUTING_KEY[str(message.routing_key)]
            event = event_type(
                patient_id=PatientId.from_string(id=body["patient_id"]),
                created_at=datetime.fromisoformat(body["created_at"]),
            )
            await self._handler.handle(event=event)
