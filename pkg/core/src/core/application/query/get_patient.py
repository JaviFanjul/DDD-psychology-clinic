from dataclasses import dataclass

from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_query_repository import (
    PatientDto,
    PatientQueryRepository,
)
from core.domain.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetPatientQuery(Query[PatientDto]):
    id: str


class GetPatientQueryHandler(QueryHandler[GetPatientQuery, PatientDto]):
    def __init__(self, repository: PatientQueryRepository) -> None:
        self._repository = repository

    def handle(self, query: GetPatientQuery) -> PatientDto:
        patient = self._repository.find_by_id(PatientId.from_string(query.id))
        if patient is None:
            raise PatientNotFound(query.id)
        return patient
