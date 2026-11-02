from dataclasses import dataclass

from core.domain.domain_event import DomainEvent
from core.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class PatientCreated(DomainEvent):
    patient_id: PatientId


@dataclass(frozen=True)
class PatientDischarged(DomainEvent):
    patient_id: PatientId
