from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto
from core.infrastructure.postgres.psychologist_mapper import PsychologistMapper


def test_given_a_psychologist_when_mapping_to_model_then_it_flattens_its_value_objects(
    psychologist, psychologist_model
):
    mapped = PsychologistMapper.to_model(psychologist=psychologist)

    assert (
        mapped.id,
        mapped.email,
        mapped.first_name,
        mapped.last_names,
        mapped.phone_prefix,
        mapped.phone_number,
        mapped.license_number,
    ) == (
        psychologist_model.id,
        psychologist_model.email,
        psychologist_model.first_name,
        psychologist_model.last_names,
        psychologist_model.phone_prefix,
        psychologist_model.phone_number,
        psychologist_model.license_number,
    )


def test_given_a_model_when_mapping_to_dto_then_it_copies_its_columns(psychologist_model):
    mapped = PsychologistMapper.to_dto(model=psychologist_model)

    assert mapped == PsychologistDto(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )
