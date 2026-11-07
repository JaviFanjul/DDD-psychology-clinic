from dataclasses import dataclass
from uuid import UUID, uuid4

from core.domain.model.psychologist.errors import InvalidPsychologistId


@dataclass(frozen=True)
class PsychologistId:
    id: UUID

    @classmethod
    def generate(cls) -> PsychologistId:
        return cls(id=uuid4())

    @classmethod
    def from_string(cls, id: str) -> PsychologistId:
        try:
            return cls(id=UUID(id))
        except ValueError as error:
            raise InvalidPsychologistId(value=id) from error

    def __str__(self) -> str:
        return str(self.id)
