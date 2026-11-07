from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_command_repository import (
    AppointmentCommandRepository,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import (
    AppointmentNotLoaded,
    AppointmentNotSaved,
    PatientAppointmentsNotLoaded,
)
from core.domain.model.patient.patient_id import PatientId
from core.infrastructure.postgres.appointment_mapper import AppointmentMapper
from core.infrastructure.postgres.appointment_model import AppointmentModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresAppointmentCommandRepository(AppointmentCommandRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, appointment: Appointment) -> None:
        try:
            await self._session.merge(AppointmentMapper.to_model(appointment=appointment))
            await self._session.commit()
        except SQLAlchemyError as error:
            await self._session.rollback()
            raise AppointmentNotSaved(id=str(appointment.id)) from error

    async def find_by_id(self, id: AppointmentId) -> Appointment | None:
        try:
            model = await self._session.get(AppointmentModel, id.id)
        except SQLAlchemyError as error:
            raise AppointmentNotLoaded(id=str(id)) from error
        if model is None:
            return None
        return AppointmentMapper.to_entity(model=model)

    async def find_pending_by_patient(self, patient_id: PatientId) -> list[Appointment]:
        statement = select(AppointmentModel).where(
            AppointmentModel.patient_id == patient_id.id,
            AppointmentModel.status == AppointmentStatus.PENDING.value,
        )
        try:
            models = (await self._session.scalars(statement)).all()
        except SQLAlchemyError as error:
            raise PatientAppointmentsNotLoaded(patient_id=str(patient_id)) from error
        return [AppointmentMapper.to_entity(model=model) for model in models]
