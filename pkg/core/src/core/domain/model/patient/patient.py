from core.domain.domain_event import DomainEvent
from core.domain.model.patient.events import PatientCreated
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone


class Patient:
    def __init__(
        self,
        id: PatientId,
        email: PatientEmail,
        name: PatientName,
        phone: PatientPhone,
        address: PatientAddress,
    ) -> None:
        self.id = id
        self.email = email
        self.name = name
        self.phone = phone
        self.address = address
        self._events: list[DomainEvent] = []

    @classmethod
    def create(
        cls,
        id: PatientId,
        email: PatientEmail,
        name: PatientName,
        phone: PatientPhone,
        address: PatientAddress,
    ) -> Patient:
        patient: Patient = cls(id=id, email=email, name=name, phone=phone, address=address)
        patient._events.append(PatientCreated(patient_id=id))
        return patient

    def pull_events(self) -> list[DomainEvent]:
        events: list[DomainEvent] = self._events
        self._events = []
        return events
