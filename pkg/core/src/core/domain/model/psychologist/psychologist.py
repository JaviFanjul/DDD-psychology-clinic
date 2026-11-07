from core.domain.domain_event import DomainEvent
from core.domain.model.psychologist.events import PsychologistCreated
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone


class Psychologist:
    def __init__(
        self,
        id: PsychologistId,
        email: PsychologistEmail,
        name: PsychologistName,
        phone: PsychologistPhone,
        license_number: PsychologistLicenseNumber,
    ) -> None:
        self._id = id
        self._email = email
        self._name = name
        self._phone = phone
        self._license_number = license_number
        self._events: list[DomainEvent] = []

    @property
    def id(self) -> PsychologistId:
        return self._id

    @property
    def email(self) -> PsychologistEmail:
        return self._email

    @property
    def name(self) -> PsychologistName:
        return self._name

    @property
    def phone(self) -> PsychologistPhone:
        return self._phone

    @property
    def license_number(self) -> PsychologistLicenseNumber:
        return self._license_number

    @classmethod
    def create(
        cls,
        id: PsychologistId,
        email: PsychologistEmail,
        name: PsychologistName,
        phone: PsychologistPhone,
        license_number: PsychologistLicenseNumber,
    ) -> Psychologist:
        psychologist: Psychologist = cls(
            id=id,
            email=email,
            name=name,
            phone=phone,
            license_number=license_number,
        )
        psychologist._events.append(PsychologistCreated(psychologist_id=id))
        return psychologist

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Psychologist) and other._id == self._id

    def __hash__(self) -> int:
        return hash(self._id)

    def pull_events(self) -> list[DomainEvent]:
        events: list[DomainEvent] = self._events
        self._events = []
        return events
