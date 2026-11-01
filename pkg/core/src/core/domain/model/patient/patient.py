from core.domain.domain_event import DomainEvent
from core.domain.model.patient.events import PatientRegistered
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId


class Patient:
    def __init__(self, id: PatientId, email: PatientEmail) -> None:
        self.id = id
        self.email = email
        self._events: list[DomainEvent] = []

    @classmethod
    def register(cls, id: PatientId, email: PatientEmail) -> Patient:
        patient: Patient = cls(id, email)
        patient._events.append(PatientRegistered(id))
        return patient

    def pull_events(self) -> list[DomainEvent]:
        events: list[DomainEvent] = self._events
        self._events = []
        return events
