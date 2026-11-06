from assistant.domain.domain_error import DomainError


class InvalidPatientId(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"{value!r} is not a valid UUID")


class PatientNotFound(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Patient {id!r} was not found")


class PatientNotActive(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Patient {id!r} is not active")


class PatientNotSaved(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Patient {id!r} could not be saved")


class PatientNotLoaded(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Patient {id!r} could not be loaded")
