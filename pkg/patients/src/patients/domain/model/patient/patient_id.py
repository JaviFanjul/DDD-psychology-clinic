from dataclasses import dataclass
from uuid import UUID, uuid4

from patients.domain.model.patient.errors import InvalidPatientId


@dataclass(frozen=True)
class PatientId:
    id: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID):
            raise InvalidPatientId(f"{self.id!r} is not a UUID")

    @classmethod
    def generate(cls) -> PatientId:
        return cls(id=uuid4())

    @classmethod
    def from_string(cls, id: str) -> PatientId:
        return cls(id=UUID(id))
