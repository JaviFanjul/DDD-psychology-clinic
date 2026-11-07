from core.domain.event_bus import EventHandler
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.events import PatientReadmitted
from core.domain.model.patient.patient_notifier import PatientNotifier
from core.domain.model.patient.patient_query_repository import (
    PatientDto,
    PatientQueryRepository,
)


class WelcomePatientBackOnPatientReadmitted(EventHandler[PatientReadmitted]):
    def __init__(self, repository: PatientQueryRepository, notifier: PatientNotifier) -> None:
        self._repository = repository
        self._notifier = notifier

    async def handle(self, event: PatientReadmitted) -> None:
        patient: PatientDto | None = await self._repository.find_by_id(id=event.patient_id)
        if patient is None:
            raise PatientNotFound(id=str(event.patient_id))
        await self._notifier.welcome_back(patient=patient)
