from http import HTTPStatus

from core.application.command.create_patient import CreatePatientCommand
from core.application.query.get_patient import GetPatientQuery
from core.domain.command_bus import CommandBus
from core.domain.domain_error import DomainError
from core.domain.model.patient.errors import (
    InvalidPatientAddress,
    InvalidPatientEmail,
    InvalidPatientId,
    InvalidPatientName,
    PatientNotFound,
    PatientNotLoaded,
    PatientNotSaved,
)
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_query_repository import PatientDto
from core.domain.query_bus import QueryBus

STATUS_BY_ERROR: dict[type[DomainError], HTTPStatus] = {
    InvalidPatientId: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPatientEmail: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPatientName: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPatientAddress: HTTPStatus.UNPROCESSABLE_CONTENT,
    PatientNotFound: HTTPStatus.NOT_FOUND,
    PatientNotSaved: HTTPStatus.INTERNAL_SERVER_ERROR,
    PatientNotLoaded: HTTPStatus.INTERNAL_SERVER_ERROR,
}


class PatientController:
    def __init__(self, command_bus: CommandBus, query_bus: QueryBus) -> None:
        self._command_bus = command_bus
        self._query_bus = query_bus

    async def create(
        self,
        email: str,
        first_name: str,
        last_names: str,
        street: str,
        postal_code: str,
        city: str,
        province: str,
    ) -> str:
        patient_id: PatientId = PatientId.generate()
        patient_email: PatientEmail = PatientEmail(value=email)
        patient_name: PatientName = PatientName(first_name=first_name, last_names=last_names)
        patient_address: PatientAddress = PatientAddress(
            street=street, postal_code=postal_code, city=city, province=province
        )
        await self._command_bus.handle(
            command=CreatePatientCommand(
                id=patient_id,
                email=patient_email,
                name=patient_name,
                address=patient_address,
            )
        )
        return str(patient_id)

    async def get(self, id: str) -> PatientDto:
        patient_id: PatientId = PatientId.from_string(id=id)
        return await self._query_bus.handle(query=GetPatientQuery(id=patient_id))
