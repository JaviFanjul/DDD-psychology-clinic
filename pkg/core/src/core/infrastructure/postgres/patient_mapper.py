from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_query_repository import PatientDto
from core.infrastructure.postgres.patient_model import PatientModel


class PatientMapper:
    @staticmethod
    def to_model(patient: Patient) -> PatientModel:
        return PatientModel(
            id=patient.id.id,
            email=patient.email.value,
            first_name=patient.name.first_name,
            last_names=patient.name.last_names,
            street=patient.address.street,
            postal_code=patient.address.postal_code,
            city=patient.address.city,
            province=patient.address.province,
        )

    @staticmethod
    def to_entity(model: PatientModel) -> Patient:
        return Patient(
            id=PatientId(id=model.id),
            email=PatientEmail(value=model.email),
            name=PatientName(first_name=model.first_name, last_names=model.last_names),
            address=PatientAddress(
                street=model.street,
                postal_code=model.postal_code,
                city=model.city,
                province=model.province,
            ),
        )

    @staticmethod
    def to_dto(model: PatientModel) -> PatientDto:
        return PatientDto(
            id=str(model.id),
            email=model.email,
            first_name=model.first_name,
            last_names=model.last_names,
            street=model.street,
            postal_code=model.postal_code,
            city=model.city,
            province=model.province,
        )
