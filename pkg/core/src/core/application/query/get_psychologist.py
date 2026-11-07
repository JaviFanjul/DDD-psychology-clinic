from dataclasses import dataclass

from core.domain.model.psychologist.errors import PsychologistNotFound
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_query_repository import (
    PsychologistDto,
    PsychologistQueryRepository,
)
from core.domain.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetPsychologistQuery(Query[PsychologistDto]):
    id: PsychologistId


class GetPsychologistQueryHandler(QueryHandler[GetPsychologistQuery, PsychologistDto]):
    def __init__(self, repository: PsychologistQueryRepository) -> None:
        self._repository = repository

    async def handle(self, query: GetPsychologistQuery) -> PsychologistDto:
        psychologist: PsychologistDto | None = await self._repository.find_by_id(id=query.id)
        if psychologist is None:
            raise PsychologistNotFound(id=str(query.id))
        return psychologist
