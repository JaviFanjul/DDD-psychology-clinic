import re
from dataclasses import dataclass

from core.domain.model.psychologist.errors import InvalidPsychologistLicenseNumber

LICENSE_NUMBER_PATTERN = re.compile(r"([A-Z]{1,2})-?([0-9]{4,6})")


@dataclass(frozen=True)
class PsychologistLicenseNumber:
    value: str

    def __post_init__(self) -> None:
        match = LICENSE_NUMBER_PATTERN.fullmatch(self.value.strip().upper())
        if match is None:
            raise InvalidPsychologistLicenseNumber()
        object.__setattr__(self, "value", f"{match.group(1)}-{match.group(2)}")
