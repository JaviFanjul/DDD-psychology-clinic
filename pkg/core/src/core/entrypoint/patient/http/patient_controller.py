from http import HTTPStatus

from core.application.command.create_patient import CreatePatientCommand
from core.application.query.get_patient import GetPatientQuery
from core.domain.command_bus import CommandBus
from core.domain.domain_error import DomainError
from core.domain.model.patient.errors import (
    InvalidPatientEmail,
    InvalidPatientId,
    PatientNotFound,
)
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_query_repository import PatientDto
from core.domain.query_bus import QueryBus

STATUS_BY_ERROR: dict[type[DomainError], HTTPStatus] = {
    InvalidPatientId: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPatientEmail: HTTPStatus.UNPROCESSABLE_CONTENT,
    PatientNotFound: HTTPStatus.NOT_FOUND,
}


class PatientController:
    def __init__(self, command_bus: CommandBus, query_bus: QueryBus) -> None:
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create(self, email: str) -> str:
        patient_id: PatientId = PatientId.generate()
        patient_email: PatientEmail = PatientEmail(email)
        self._command_bus.handle(CreatePatientCommand(id=patient_id, email=patient_email))
        return str(patient_id)

    def get(self, id: str) -> PatientDto:
        patient_id: PatientId = PatientId.from_string(id)
        return self._query_bus.handle(GetPatientQuery(id=patient_id))
