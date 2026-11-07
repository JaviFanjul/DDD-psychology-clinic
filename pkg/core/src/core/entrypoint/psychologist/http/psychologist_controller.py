from http import HTTPStatus

from core.application.psychologist.command.create_psychologist import CreatePsychologistCommand
from core.application.psychologist.query.get_psychologist import GetPsychologistQuery
from core.domain.command_bus import CommandBus
from core.domain.domain_error import DomainError
from core.domain.model.psychologist.errors import (
    InvalidPsychologistEmail,
    InvalidPsychologistId,
    InvalidPsychologistLicenseNumber,
    InvalidPsychologistName,
    InvalidPsychologistPhone,
    PsychologistNotFound,
    PsychologistNotLoaded,
    PsychologistNotSaved,
)
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone
from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto
from core.domain.query_bus import QueryBus

STATUS_BY_ERROR: dict[type[DomainError], HTTPStatus] = {
    InvalidPsychologistId: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPsychologistEmail: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPsychologistName: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPsychologistPhone: HTTPStatus.UNPROCESSABLE_CONTENT,
    InvalidPsychologistLicenseNumber: HTTPStatus.UNPROCESSABLE_CONTENT,
    PsychologistNotFound: HTTPStatus.NOT_FOUND,
    PsychologistNotSaved: HTTPStatus.INTERNAL_SERVER_ERROR,
    PsychologistNotLoaded: HTTPStatus.INTERNAL_SERVER_ERROR,
}


class PsychologistController:
    def __init__(self, command_bus: CommandBus, query_bus: QueryBus) -> None:
        self._command_bus = command_bus
        self._query_bus = query_bus

    async def create(
        self,
        email: str,
        first_name: str,
        last_names: str,
        phone_prefix: str,
        phone_number: str,
        license_number: str,
    ) -> str:
        psychologist_id: PsychologistId = PsychologistId.generate()
        psychologist_email: PsychologistEmail = PsychologistEmail(value=email)
        psychologist_name: PsychologistName = PsychologistName(first_name=first_name, last_names=last_names)
        psychologist_phone: PsychologistPhone = PsychologistPhone(prefix=phone_prefix, number=phone_number)
        psychologist_license_number: PsychologistLicenseNumber = PsychologistLicenseNumber(value=license_number)
        await self._command_bus.handle(
            command=CreatePsychologistCommand(
                id=psychologist_id,
                email=psychologist_email,
                name=psychologist_name,
                phone=psychologist_phone,
                license_number=psychologist_license_number,
            )
        )
        return str(psychologist_id)

    async def get(self, id: str) -> PsychologistDto:
        psychologist_id: PsychologistId = PsychologistId.from_string(id=id)
        return await self._query_bus.handle(query=GetPsychologistQuery(id=psychologist_id))
