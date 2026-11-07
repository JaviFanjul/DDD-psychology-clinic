from dataclasses import dataclass

from core.domain.domain_event import DomainEvent
from core.domain.model.psychologist.psychologist_id import PsychologistId


@dataclass(frozen=True)
class PsychologistCreated(DomainEvent):
    psychologist_id: PsychologistId
