from core.domain.model.psychologist.errors import PsychologistNotSaved
from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_command_repository import (
    PsychologistCommandRepository,
)
from core.infrastructure.postgres.psychologist_mapper import PsychologistMapper
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresPsychologistCommandRepository(PsychologistCommandRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, psychologist: Psychologist) -> None:
        try:
            await self._session.merge(PsychologistMapper.to_model(psychologist=psychologist))
            await self._session.commit()
        except SQLAlchemyError as error:
            await self._session.rollback()
            raise PsychologistNotSaved(id=str(psychologist.id)) from error
