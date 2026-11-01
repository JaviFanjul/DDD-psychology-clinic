from abc import ABC, abstractmethod

from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_id import PatientId


class PatientCommandRepository(ABC):
    @abstractmethod
    def save(self, patient: Patient) -> None: ...

    @abstractmethod
    def find_by_id(self, id: PatientId) -> Patient | None: ...
