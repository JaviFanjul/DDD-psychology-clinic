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
        self._id = id
        self._email = email
        self._name = name
        self._phone = phone
        self._address = address
        self._status = status
        self._events: list[DomainEvent] = []

    @property
    def id(self) -> PatientId:
        return self._id

    @property
    def email(self) -> PatientEmail:
        return self._email

    @property
    def name(self) -> PatientName:
        return self._name

    @property
    def phone(self) -> PatientPhone:
        return self._phone

    @property
    def address(self) -> PatientAddress:
        return self._address

    @property
    def status(self) -> PatientStatus:
        return self._status

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
        if self._status is PatientStatus.DISCHARGED:
            raise PatientAlreadyDischarged(id=str(self._id))
        self._status = PatientStatus.DISCHARGED
        self._events.append(PatientDischarged(patient_id=self._id))

    def readmit(self) -> None:
        if self._status is PatientStatus.ACTIVE:
            raise PatientAlreadyActive(id=str(self._id))
        self._status = PatientStatus.ACTIVE
        self._events.append(PatientReadmitted(patient_id=self._id))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Patient) and other._id == self._id

    def __hash__(self) -> int:
        return hash(self._id)

    def pull_events(self) -> list[DomainEvent]:
        events: list[DomainEvent] = self._events
        self._events = []
        return events
