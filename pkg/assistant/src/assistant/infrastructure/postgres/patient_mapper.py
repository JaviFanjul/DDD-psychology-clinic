from assistant.domain.model.patient.patient import Patient
from assistant.domain.model.patient.patient_id import PatientId
from assistant.infrastructure.postgres.patient_model import PatientModel


class PatientMapper:
    @staticmethod
    def to_model(patient: Patient) -> PatientModel:
        return PatientModel(id=patient.id.id, active=patient.is_active)

    @staticmethod
    def to_entity(model: PatientModel) -> Patient:
        return Patient(id=PatientId(id=model.id), active=model.active)
