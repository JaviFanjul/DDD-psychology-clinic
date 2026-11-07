from core.domain.model.patient.patient_query_repository import PatientDto
from core.domain.model.patient.patient_status import PatientStatus
from core.infrastructure.postgres.patient_mapper import PatientMapper


def test_given_a_patient_when_mapping_to_model_then_it_flattens_its_value_objects(patient, model):
    mapped = PatientMapper.to_model(patient=patient)

    assert (
        mapped.id,
        mapped.email,
        mapped.first_name,
        mapped.last_names,
        mapped.phone_prefix,
        mapped.phone_number,
        mapped.street,
        mapped.postal_code,
        mapped.city,
        mapped.province,
        mapped.status,
    ) == (
        model.id,
        model.email,
        model.first_name,
        model.last_names,
        model.phone_prefix,
        model.phone_number,
        model.street,
        model.postal_code,
        model.city,
        model.province,
        model.status,
    )


def test_given_a_model_when_mapping_to_entity_then_it_rebuilds_the_patient_without_events(model, patient):
    mapped = PatientMapper.to_entity(model=model)

    assert mapped.id == patient.id
    assert mapped.email == patient.email
    assert mapped.name == patient.name
    assert mapped.phone == patient.phone
    assert mapped.address == patient.address
    assert mapped.status is PatientStatus.ACTIVE
    assert mapped.pull_events() == []


def test_given_a_model_when_mapping_to_dto_then_it_copies_its_columns(model):
    mapped = PatientMapper.to_dto(model=model)

    assert mapped == PatientDto(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        email="ana@gmail.com",
        first_name="Ana",
        last_names="García López",
        phone_prefix="+34",
        phone_number="612345678",
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
        status="active",
    )


def test_given_a_discharged_patient_when_mapping_to_model_and_back_then_it_keeps_its_status(
    patient,
):
    patient.discharge()

    mapped = PatientMapper.to_entity(model=PatientMapper.to_model(patient=patient))

    assert mapped.status is PatientStatus.DISCHARGED
