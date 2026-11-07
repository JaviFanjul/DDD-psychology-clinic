import json
from datetime import datetime
from typing import Any

from core.domain.domain_event import DomainEvent
from core.domain.model.patient.events import (
    PatientCreated,
    PatientDischarged,
    PatientReadmitted,
)
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.events import PsychologistCreated
from core.domain.model.psychologist.psychologist_id import PsychologistId

type PatientEvent = PatientCreated | PatientDischarged | PatientReadmitted

PATIENT_EVENT_TYPES: dict[str, type[PatientEvent]] = {
    "patient.created": PatientCreated,
    "patient.discharged": PatientDischarged,
    "patient.readmitted": PatientReadmitted,
}
PSYCHOLOGIST_EVENT_TYPES: dict[str, type[PsychologistCreated]] = {
    "psychologist.created": PsychologistCreated,
}
ROUTING_KEYS: dict[type[DomainEvent], str] = {
    event_type: routing_key
    for routing_key, event_type in (PATIENT_EVENT_TYPES | PSYCHOLOGIST_EVENT_TYPES).items()
}


class RabbitMqEventSerializer:
    @staticmethod
    def to_message(event: DomainEvent) -> tuple[str, bytes]:
        body: dict[str, Any]
        if isinstance(event, PatientCreated | PatientDischarged | PatientReadmitted):
            body = {"patient_id": str(event.patient_id)}
        elif isinstance(event, PsychologistCreated):
            body = {"psychologist_id": str(event.psychologist_id)}
        else:
            raise TypeError(f"{type(event).__name__} cannot be serialized")
        body["created_at"] = event.created_at.isoformat()
        return ROUTING_KEYS[type(event)], json.dumps(body).encode()

    @staticmethod
    def from_message(routing_key: str, body: bytes) -> DomainEvent:
        data = json.loads(body)
        created_at = datetime.fromisoformat(data["created_at"])
        event: DomainEvent
        if routing_key in PSYCHOLOGIST_EVENT_TYPES:
            event = PSYCHOLOGIST_EVENT_TYPES[routing_key](
                psychologist_id=PsychologistId.from_string(id=data["psychologist_id"]),
                created_at=created_at,
            )
        else:
            event = PATIENT_EVENT_TYPES[routing_key](
                patient_id=PatientId.from_string(id=data["patient_id"]),
                created_at=created_at,
            )
        return event
