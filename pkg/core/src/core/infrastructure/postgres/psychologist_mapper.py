from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto
from core.infrastructure.postgres.psychologist_model import PsychologistModel


class PsychologistMapper:
    @staticmethod
    def to_model(psychologist: Psychologist) -> PsychologistModel:
        return PsychologistModel(
            id=psychologist.id.id,
            email=psychologist.email.value,
            first_name=psychologist.name.first_name,
            last_names=psychologist.name.last_names,
            phone_prefix=psychologist.phone.prefix,
            phone_number=psychologist.phone.number,
            license_number=psychologist.license_number.value,
        )

    @staticmethod
    def to_dto(model: PsychologistModel) -> PsychologistDto:
        return PsychologistDto(
            id=str(model.id),
            email=model.email,
            first_name=model.first_name,
            last_names=model.last_names,
            phone_prefix=model.phone_prefix,
            phone_number=model.phone_number,
            license_number=model.license_number,
        )
