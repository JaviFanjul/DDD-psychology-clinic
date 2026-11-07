from dataclasses import dataclass
from uuid import UUID, uuid4

from core.domain.model.appointment.errors import InvalidAppointmentId


@dataclass(frozen=True)
class AppointmentId:
    id: UUID

    @classmethod
    def generate(cls) -> AppointmentId:
        return cls(id=uuid4())

    @classmethod
    def from_string(cls, id: str) -> AppointmentId:
        try:
            return cls(id=UUID(id))
        except ValueError as error:
            raise InvalidAppointmentId(value=id) from error

    def __str__(self) -> str:
        return str(self.id)
