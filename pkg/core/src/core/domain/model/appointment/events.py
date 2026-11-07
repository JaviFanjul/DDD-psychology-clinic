from dataclasses import dataclass

from core.domain.domain_event import DomainEvent
from core.domain.model.appointment.appointment_id import AppointmentId


@dataclass(frozen=True)
class AppointmentScheduled(DomainEvent):
    appointment_id: AppointmentId


@dataclass(frozen=True)
class AppointmentRescheduled(DomainEvent):
    appointment_id: AppointmentId


@dataclass(frozen=True)
class AppointmentModalityChanged(DomainEvent):
    appointment_id: AppointmentId


@dataclass(frozen=True)
class AppointmentCancelled(DomainEvent):
    appointment_id: AppointmentId


@dataclass(frozen=True)
class AppointmentCompleted(DomainEvent):
    appointment_id: AppointmentId
