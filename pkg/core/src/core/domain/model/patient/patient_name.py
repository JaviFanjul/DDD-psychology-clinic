from dataclasses import dataclass

from core.domain.model.patient.errors import InvalidPatientName


@dataclass(frozen=True)
class PatientName:
    first_name: str
    last_names: str

    def __post_init__(self) -> None:
        first_name = self.first_name.strip()
        last_names = self.last_names.strip()
        if not first_name or not last_names:
            raise InvalidPatientName()
        object.__setattr__(self, "first_name", first_name)
        object.__setattr__(self, "last_names", last_names)
