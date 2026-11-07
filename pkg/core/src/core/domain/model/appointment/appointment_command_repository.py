from abc import ABC, abstractmethod

from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.patient.patient_id import PatientId


class AppointmentCommandRepository(ABC):
    @abstractmethod
    async def save(self, appointment: Appointment) -> None: ...

    @abstractmethod
    async def find_by_id(self, id: AppointmentId) -> Appointment | None: ...

    @abstractmethod
    async def find_pending_by_patient(self, patient_id: PatientId) -> list[Appointment]: ...
