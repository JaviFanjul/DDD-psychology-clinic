from http import HTTPStatus

from core.application.command.register_patient import RegisterPatientCommand
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

    def register(self, email: str) -> str:
        id = PatientId.generate()
        self._command_bus.handle(RegisterPatientCommand(id=id, email=PatientEmail(email)))
        return str(id.id)

    def get(self, id: str) -> PatientDto:
        return self._query_bus.handle(GetPatientQuery(id=id))
