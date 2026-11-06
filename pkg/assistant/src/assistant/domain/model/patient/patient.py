from assistant.domain.model.patient.patient_id import PatientId


class Patient:
    def __init__(self, id: PatientId, active: bool) -> None:
        self._id = id
        self._active = active

    @property
    def id(self) -> PatientId:
        return self._id

    @property
    def is_active(self) -> bool:
        return self._active

    @classmethod
    def create(cls, id: PatientId) -> Patient:
        patient: Patient = cls(id=id, active=True)
        return patient

    def activate(self) -> None:
        self._active = True

    def deactivate(self) -> None:
        self._active = False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Patient) and other._id == self._id

    def __hash__(self) -> int:
        return hash(self._id)
