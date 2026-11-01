import re
from dataclasses import dataclass

from core.domain.model.patient.errors import InvalidPatientAddress

POSTAL_CODE_PATTERN = re.compile(r"[0-9]{5}")


@dataclass(frozen=True)
class PatientAddress:
    street: str
    postal_code: str
    city: str
    province: str

    def __post_init__(self) -> None:
        street = self.street.strip()
        postal_code = self.postal_code.strip()
        city = self.city.strip()
        province = self.province.strip()
        if not street or not city or not province:
            raise InvalidPatientAddress()
        if not POSTAL_CODE_PATTERN.fullmatch(postal_code):
            raise InvalidPatientAddress()
        object.__setattr__(self, "street", street)
        object.__setattr__(self, "postal_code", postal_code)
        object.__setattr__(self, "city", city)
        object.__setattr__(self, "province", province)
