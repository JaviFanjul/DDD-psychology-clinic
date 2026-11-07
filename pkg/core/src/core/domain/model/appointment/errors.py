from core.domain.domain_error import DomainError


class InvalidAppointmentId(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"{value!r} is not a valid UUID")


class InvalidAppointmentSlot(DomainError):
    def __init__(self) -> None:
        super().__init__("The appointment slot is not valid")


class InvalidAppointmentModality(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"{value!r} is not a valid appointment modality")


class AppointmentNotFound(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Appointment {id!r} was not found")


class AppointmentNotSaved(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Appointment {id!r} could not be saved")


class AppointmentNotLoaded(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Appointment {id!r} could not be loaded")


class AppointmentAlreadyCancelled(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Appointment {id!r} is already cancelled")


class AppointmentAlreadyCompleted(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Appointment {id!r} is already completed")


class AppointmentOverlaps(DomainError):
    def __init__(self, psychologist_id: str) -> None:
        super().__init__(
            f"Psychologist {psychologist_id!r} already has a pending appointment at that time"
        )


class PatientAppointmentsNotLoaded(DomainError):
    def __init__(self, patient_id: str) -> None:
        super().__init__(f"Appointments of patient {patient_id!r} could not be loaded")


class PsychologistAppointmentsNotLoaded(DomainError):
    def __init__(self, psychologist_id: str) -> None:
        super().__init__(f"Appointments of psychologist {psychologist_id!r} could not be loaded")
