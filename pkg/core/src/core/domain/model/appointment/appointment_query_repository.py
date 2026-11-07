from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.psychologist.psychologist_id import PsychologistId


@dataclass(frozen=True)
class AppointmentDto:
    id: str
    patient_id: str
    psychologist_id: str
    starts_at: datetime
    duration_minutes: int
    modality: str
    status: str


class AppointmentQueryRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: AppointmentId) -> AppointmentDto | None: ...

    @abstractmethod
    async def find_pending_slots(
        self, psychologist_id: PsychologistId, excluding: AppointmentId
    ) -> list[AppointmentSlot]: ...
