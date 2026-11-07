import re
from dataclasses import dataclass

from core.domain.model.psychologist.errors import InvalidPsychologistPhone

PREFIX_PATTERN = re.compile(r"\+?([1-9][0-9]{0,2})")
NUMBER_PATTERN = re.compile(r"[0-9]{4,14}")
NUMBER_SEPARATORS_PATTERN = re.compile(r"[ \-.()]")
MAX_DIGITS = 15


@dataclass(frozen=True)
class PsychologistPhone:
    prefix: str
    number: str

    def __post_init__(self) -> None:
        prefix_match = PREFIX_PATTERN.fullmatch(self.prefix.strip())
        number = NUMBER_SEPARATORS_PATTERN.sub("", self.number.strip())
        if prefix_match is None or not NUMBER_PATTERN.fullmatch(number):
            raise InvalidPsychologistPhone()
        prefix = prefix_match.group(1)
        if len(prefix) + len(number) > MAX_DIGITS:
            raise InvalidPsychologistPhone()
        object.__setattr__(self, "prefix", f"+{prefix}")
        object.__setattr__(self, "number", number)
