from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.domain.model.psychologist.psychologist_id import PsychologistId


@dataclass(frozen=True)
class PsychologistDto:
    id: str
    email: str
    first_name: str
    last_names: str
    phone_prefix: str
    phone_number: str
    license_number: str


class PsychologistQueryRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: PsychologistId) -> PsychologistDto | None: ...
