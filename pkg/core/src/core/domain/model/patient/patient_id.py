from dataclasses import dataclass
from uuid import UUID, uuid4

from core.domain.model.patient.errors import InvalidPatientId


@dataclass(frozen=True)
class PatientId:
    id: UUID

    @classmethod
    def generate(cls) -> PatientId:
        return cls(id=uuid4())

    @classmethod
    def from_string(cls, id: str) -> PatientId:
        try:
            return cls(id=UUID(id))
        except ValueError as error:
            raise InvalidPatientId(value=id) from error

    def __str__(self) -> str:
        return str(self.id)
