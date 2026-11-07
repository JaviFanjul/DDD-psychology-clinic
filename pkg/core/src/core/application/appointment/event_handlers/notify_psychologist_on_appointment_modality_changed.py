from core.domain.event_bus import EventHandler
from core.domain.model.appointment.appointment_query_repository import (
    AppointmentDto,
    AppointmentQueryRepository,
)
from core.domain.model.appointment.errors import AppointmentNotFound
from core.domain.model.appointment.events import AppointmentModalityChanged
from core.domain.model.psychologist.errors import PsychologistNotFound
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_notifier import PsychologistNotifier
from core.domain.model.psychologist.psychologist_query_repository import (
    PsychologistDto,
    PsychologistQueryRepository,
)


class NotifyPsychologistOnAppointmentModalityChanged(EventHandler[AppointmentModalityChanged]):
    def __init__(
        self,
        appointments: AppointmentQueryRepository,
        psychologists: PsychologistQueryRepository,
        notifier: PsychologistNotifier,
    ) -> None:
        self._appointments = appointments
        self._psychologists = psychologists
        self._notifier = notifier

    async def handle(self, event: AppointmentModalityChanged) -> None:
        appointment: AppointmentDto | None = await self._appointments.find_by_id(
            id=event.appointment_id
        )
        if appointment is None:
            raise AppointmentNotFound(id=str(event.appointment_id))
        psychologist_id: PsychologistId = PsychologistId.from_string(id=appointment.psychologist_id)
        psychologist: PsychologistDto | None = await self._psychologists.find_by_id(
            id=psychologist_id
        )
        if psychologist is None:
            raise PsychologistNotFound(id=appointment.psychologist_id)
        await self._notifier.appointment_modality_changed(
            psychologist=psychologist, appointment=appointment
        )
