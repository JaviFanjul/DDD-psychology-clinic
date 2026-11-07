import re
from dataclasses import dataclass

from core.domain.model.psychologist.errors import InvalidPsychologistEmail

EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s.]+(\.[^@\s.]+)+")


@dataclass(frozen=True)
class PsychologistEmail:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(normalized):
            raise InvalidPsychologistEmail()
        object.__setattr__(self, "value", normalized)
