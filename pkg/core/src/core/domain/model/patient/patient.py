from core.domain.domain_event import DomainEvent
from core.domain.model.patient.errors import PatientAlreadyActive, PatientAlreadyDischarged
from core.domain.model.patient.events import (
    PatientCreated,
    PatientDischarged,
    PatientReadmitted,
)
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone
from core.domain.model.patient.patient_status import PatientStatus


class Patient:
    def __init__(
        self,
        id: PatientId,
        email: PatientEmail,
        name: PatientName,
        phone: PatientPhone,
        address: PatientAddress,
        status: PatientStatus,
    ) -> None:
        self.id = id
        self.email = email
        self.name = name
        self.phone = phone
        self.address = address
        self.status = status
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
        patient: Patient = cls(
            id=id,
            email=email,
            name=name,
            phone=phone,
            address=address,
            status=PatientStatus.ACTIVE,
        )
        patient._events.append(PatientCreated(patient_id=id))
        return patient

    def discharge(self) -> None:
        if self.status is PatientStatus.DISCHARGED:
            raise PatientAlreadyDischarged(id=str(self.id))
        self.status = PatientStatus.DISCHARGED
        self._events.append(PatientDischarged(patient_id=self.id))

    def readmit(self) -> None:
        if self.status is PatientStatus.ACTIVE:
            raise PatientAlreadyActive(id=str(self.id))
        self.status = PatientStatus.ACTIVE
        self._events.append(PatientReadmitted(patient_id=self.id))

    def pull_events(self) -> list[DomainEvent]:
        events: list[DomainEvent] = self._events
        self._events = []
        return events
