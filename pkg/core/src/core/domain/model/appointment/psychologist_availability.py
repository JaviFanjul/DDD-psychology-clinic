from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_query_repository import AppointmentQueryRepository
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.psychologist.psychologist_id import PsychologistId


class PsychologistAvailability:
    def __init__(self, repository: AppointmentQueryRepository) -> None:
        self._repository = repository

    async def is_available(
        self, psychologist_id: PsychologistId, slot: AppointmentSlot, excluding: AppointmentId
    ) -> bool:
        busy_slots: list[AppointmentSlot] = await self._repository.find_pending_slots(
            psychologist_id=psychologist_id, excluding=excluding
        )
        return not any(slot.overlaps(other=busy_slot) for busy_slot in busy_slots)
