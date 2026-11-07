from core.domain.model.psychologist.errors import PsychologistNotLoaded
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_query_repository import (
    PsychologistDto,
    PsychologistQueryRepository,
)
from core.infrastructure.postgres.psychologist_mapper import PsychologistMapper
from core.infrastructure.postgres.psychologist_model import PsychologistModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresPsychologistQueryRepository(PsychologistQueryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, id: PsychologistId) -> PsychologistDto | None:
        try:
            model = await self._session.get(PsychologistModel, id.id)
        except SQLAlchemyError as error:
            raise PsychologistNotLoaded(id=str(id)) from error
        if model is None:
            return None
        return PsychologistMapper.to_dto(model=model)
