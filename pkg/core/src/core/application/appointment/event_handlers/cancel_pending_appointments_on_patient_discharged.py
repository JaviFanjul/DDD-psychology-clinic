from core.domain.domain_event import DomainEvent
from core.domain.event_bus import EventBus, EventHandler
from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_command_repository import (
    AppointmentCommandRepository,
)
from core.domain.model.patient.events import PatientDischarged
from core.domain.unit_of_work import UnitOfWork


class CancelPendingAppointmentsOnPatientDischarged(EventHandler[PatientDischarged]):
    def __init__(self, repository: AppointmentCommandRepository, unit_of_work: UnitOfWork, event_bus: EventBus) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._event_bus = event_bus

    async def handle(self, event: PatientDischarged) -> None:
        events: list[DomainEvent] = []
        async with self._unit_of_work:
            appointments: list[Appointment] = await self._repository.find_pending_by_patient(
                patient_id=event.patient_id
            )
            for appointment in appointments:
                appointment.cancel()
                await self._repository.save(appointment=appointment)
                events.extend(appointment.pull_events())
            await self._unit_of_work.commit()
        await self._event_bus.publish(events=events)
