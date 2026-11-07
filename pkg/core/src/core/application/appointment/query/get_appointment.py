from dataclasses import dataclass

from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_query_repository import (
    AppointmentDto,
    AppointmentQueryRepository,
)
from core.domain.model.appointment.errors import AppointmentNotFound
from core.domain.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetAppointmentQuery(Query[AppointmentDto]):
    id: AppointmentId


class GetAppointmentQueryHandler(QueryHandler[GetAppointmentQuery, AppointmentDto]):
    def __init__(self, repository: AppointmentQueryRepository) -> None:
        self._repository = repository

    async def handle(self, query: GetAppointmentQuery) -> AppointmentDto:
        appointment: AppointmentDto | None = await self._repository.find_by_id(id=query.id)
        if appointment is None:
            raise AppointmentNotFound(id=str(query.id))
        return appointment
