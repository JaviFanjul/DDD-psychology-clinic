from core.domain.model.patient.errors import PatientNotLoaded
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_query_repository import (
    PatientDto,
    PatientQueryRepository,
)
from core.infrastructure.postgres.patient_mapper import PatientMapper
from core.infrastructure.postgres.patient_model import PatientModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresPatientQueryRepository(PatientQueryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, id: PatientId) -> PatientDto | None:
        try:
            model = await self._session.get(PatientModel, id.id)
        except SQLAlchemyError as error:
            raise PatientNotLoaded(id=str(id)) from error
        if model is None:
            return None
        return PatientMapper.to_dto(model=model)
