import json
from datetime import datetime

from core.domain.domain_event import DomainEvent
from core.domain.model.patient.events import (
    PatientCreated,
    PatientDischarged,
    PatientReadmitted,
)
from core.domain.model.patient.patient_id import PatientId

EVENT_TYPES: dict[str, type[PatientCreated | PatientDischarged | PatientReadmitted]] = {
    "patient.created": PatientCreated,
    "patient.discharged": PatientDischarged,
    "patient.readmitted": PatientReadmitted,
}
ROUTING_KEYS: dict[type[DomainEvent], str] = {
    event_type: routing_key for routing_key, event_type in EVENT_TYPES.items()
}


class RabbitMqEventSerializer:
    @staticmethod
    def to_message(event: DomainEvent) -> tuple[str, bytes]:
        if not isinstance(event, PatientCreated | PatientDischarged | PatientReadmitted):
            raise TypeError(f"{type(event).__name__} cannot be serialized")
        body = {"patient_id": str(event.patient_id), "created_at": event.created_at.isoformat()}
        return ROUTING_KEYS[type(event)], json.dumps(body).encode()

    @staticmethod
    def from_message(routing_key: str, body: bytes) -> DomainEvent:
        data = json.loads(body)
        event: DomainEvent = EVENT_TYPES[routing_key](
            patient_id=PatientId.from_string(id=data["patient_id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
        return event
