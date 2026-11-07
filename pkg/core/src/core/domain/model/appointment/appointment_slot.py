from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from core.domain.model.appointment.errors import InvalidAppointmentSlot


@dataclass(frozen=True)
class AppointmentSlot:
    starts_at: datetime
    duration_minutes: int

    def __post_init__(self) -> None:
        if self.starts_at.utcoffset() is None or self.duration_minutes <= 0:
            raise InvalidAppointmentSlot()
        object.__setattr__(self, "starts_at", self.starts_at.astimezone(UTC))

    @property
    def ends_at(self) -> datetime:
        return self.starts_at + timedelta(minutes=self.duration_minutes)

    def overlaps(self, other: AppointmentSlot) -> bool:
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at
