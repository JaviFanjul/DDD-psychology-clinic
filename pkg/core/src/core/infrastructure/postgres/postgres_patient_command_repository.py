from core.domain.model.patient.errors import PatientNotLoaded, PatientNotSaved
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_command_repository import PatientCommandRepository
from core.domain.model.patient.patient_id import PatientId
from core.infrastructure.postgres.patient_mapper import PatientMapper
from core.infrastructure.postgres.patient_model import PatientModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresPatientCommandRepository(PatientCommandRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, patient: Patient) -> None:
        try:
            await self._session.merge(PatientMapper.to_model(patient=patient))
            await self._session.commit()
        except SQLAlchemyError as error:
            await self._session.rollback()
            raise PatientNotSaved(id=str(patient.id)) from error

    async def find_by_id(self, id: PatientId) -> Patient | None:
        try:
            model = await self._session.get(PatientModel, id.id)
        except SQLAlchemyError as error:
            raise PatientNotLoaded(id=str(id)) from error
        if model is None:
            return None
        return PatientMapper.to_entity(model=model)
