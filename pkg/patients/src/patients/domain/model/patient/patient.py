from patients.domain.domain_event import DomainEvent
from patients.domain.model.patient.events import PatientRegistered
from patients.domain.model.patient.patient_id import PatientId


class Patient:
    def __init__(self, id: PatientId) -> None:
        self.id = id
        self._events: list[DomainEvent] = []

    @classmethod
    def register(cls, id: PatientId) -> Patient:
        patient = cls(id)
        patient._events.append(PatientRegistered(id))
        return patient

    def pull_events(self) -> list[DomainEvent]:
        events = self._events
        self._events = []
        return events
