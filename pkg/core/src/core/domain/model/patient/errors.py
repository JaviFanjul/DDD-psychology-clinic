from core.domain.domain_error import DomainError


class InvalidPatientId(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"{value!r} is not a valid UUID")


class InvalidPatientEmail(DomainError):
    def __init__(self) -> None:
        super().__init__("The patient email is not valid")
