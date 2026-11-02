from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.domain.model.patient.patient_id import PatientId


@dataclass(frozen=True)
class PatientDto:
    id: str
    email: str
    first_name: str
    last_names: str
    street: str
    postal_code: str
    city: str
    province: str


class PatientQueryRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: PatientId) -> PatientDto | None: ...
