from core.domain.domain_error import DomainError


class InvalidPatientId(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"{value!r} is not a valid UUID")


class InvalidPatientEmail(DomainError):
    def __init__(self) -> None:
        super().__init__("The patient email is not valid")


class InvalidPatientName(DomainError):
    def __init__(self) -> None:
        super().__init__("The patient name is not valid")


class InvalidPatientAddress(DomainError):
    def __init__(self) -> None:
        super().__init__("The patient address is not valid")


class PatientNotFound(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Patient {id!r} was not found")


class PatientNotSaved(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Patient {id!r} could not be saved")


class PatientNotLoaded(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Patient {id!r} could not be loaded")
