import re
from dataclasses import dataclass

from core.domain.model.patient.errors import InvalidPatientEmail

EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s.]+(\.[^@\s.]+)+")


@dataclass(frozen=True)
class PatientEmail:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(normalized):
            raise InvalidPatientEmail()
        object.__setattr__(self, "value", normalized)
