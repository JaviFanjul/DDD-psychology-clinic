from enum import StrEnum

from core.domain.model.appointment.errors import InvalidAppointmentModality


class AppointmentModality(StrEnum):
    IN_PERSON = "in_person"
    ONLINE = "online"

    @classmethod
    def from_string(cls, value: str) -> AppointmentModality:
        try:
            return cls(value)
        except ValueError as error:
            raise InvalidAppointmentModality(value=value) from error
