from abc import ABC, abstractmethod

from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto


class PsychologistNotifier(ABC):
    @abstractmethod
    async def appointment_scheduled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None: ...

    @abstractmethod
    async def appointment_rescheduled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None: ...

    @abstractmethod
    async def appointment_modality_changed(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None: ...

    @abstractmethod
    async def appointment_cancelled(
        self, psychologist: PsychologistDto, appointment: AppointmentDto
    ) -> None: ...
