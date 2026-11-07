from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_query_repository import (
    AppointmentDto,
    AppointmentQueryRepository,
)
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import (
    AppointmentNotLoaded,
    PsychologistAppointmentsNotLoaded,
)
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.infrastructure.postgres.appointment_mapper import AppointmentMapper
from core.infrastructure.postgres.appointment_model import AppointmentModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresAppointmentQueryRepository(AppointmentQueryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, id: AppointmentId) -> AppointmentDto | None:
        try:
            model = await self._session.get(AppointmentModel, id.id)
        except SQLAlchemyError as error:
            raise AppointmentNotLoaded(id=str(id)) from error
        if model is None:
            return None
        return AppointmentMapper.to_dto(model=model)

    async def find_pending_slots(
        self, psychologist_id: PsychologistId, excluding: AppointmentId
    ) -> list[AppointmentSlot]:
        statement = select(AppointmentModel.starts_at, AppointmentModel.duration_minutes).where(
            AppointmentModel.psychologist_id == psychologist_id.id,
            AppointmentModel.status == AppointmentStatus.PENDING.value,
            AppointmentModel.id != excluding.id,
        )
        try:
            rows = (await self._session.execute(statement)).all()
        except SQLAlchemyError as error:
            raise PsychologistAppointmentsNotLoaded(psychologist_id=str(psychologist_id)) from error
        return [
            AppointmentSlot(starts_at=starts_at, duration_minutes=duration_minutes)
            for starts_at, duration_minutes in rows
        ]
