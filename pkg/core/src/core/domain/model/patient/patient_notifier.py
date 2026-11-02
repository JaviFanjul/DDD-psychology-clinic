from abc import ABC, abstractmethod

from core.domain.model.patient.patient_query_repository import PatientDto


class PatientNotifier(ABC):
    @abstractmethod
    async def welcome(self, patient: PatientDto) -> None: ...

    @abstractmethod
    async def farewell(self, patient: PatientDto) -> None: ...
