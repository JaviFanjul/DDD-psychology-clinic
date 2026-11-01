from abc import ABC, abstractmethod
from dataclasses import dataclass

from patients.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class PatientDto:
    id: str
    email: str


class PatientQueryRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: PatientId) -> PatientDto | None: ...
