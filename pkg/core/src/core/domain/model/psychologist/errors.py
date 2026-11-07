from core.domain.domain_error import DomainError


class InvalidPsychologistId(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"{value!r} is not a valid UUID")


class InvalidPsychologistEmail(DomainError):
    def __init__(self) -> None:
        super().__init__("The psychologist email is not valid")


class InvalidPsychologistName(DomainError):
    def __init__(self) -> None:
        super().__init__("The psychologist name is not valid")


class InvalidPsychologistPhone(DomainError):
    def __init__(self) -> None:
        super().__init__("The psychologist phone is not valid")


class InvalidPsychologistLicenseNumber(DomainError):
    def __init__(self) -> None:
        super().__init__("The psychologist license number is not valid")


class PsychologistNotFound(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Psychologist {id!r} was not found")


class PsychologistNotSaved(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Psychologist {id!r} could not be saved")


class PsychologistNotLoaded(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Psychologist {id!r} could not be loaded")
