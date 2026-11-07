from abc import ABC, abstractmethod

from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.patient.patient_query_repository import PatientDto


class PatientNotifier(ABC):
    @abstractmethod
    async def welcome(self, patient: PatientDto) -> None: ...

    @abstractmethod
    async def welcome_back(self, patient: PatientDto) -> None: ...

    @abstractmethod
    async def farewell(self, patient: PatientDto) -> None: ...

    @abstractmethod
    async def appointment_scheduled(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None: ...

    @abstractmethod
    async def appointment_rescheduled(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None: ...

    @abstractmethod
    async def appointment_modality_changed(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None: ...

    @abstractmethod
    async def appointment_cancelled(
        self, patient: PatientDto, appointment: AppointmentDto
    ) -> None: ...

    @abstractmethod
    async def request_feedback(self, patient: PatientDto, appointment: AppointmentDto) -> None: ...
