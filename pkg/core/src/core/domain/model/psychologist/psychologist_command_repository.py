from abc import ABC, abstractmethod

from core.domain.model.psychologist.psychologist import Psychologist


class PsychologistCommandRepository(ABC):
    @abstractmethod
    async def save(self, psychologist: Psychologist) -> None: ...
