from dataclasses import dataclass

from patients.domain.domain_event import DomainEvent
from patients.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class PatientRegistered(DomainEvent):
    patient_id: PatientId
