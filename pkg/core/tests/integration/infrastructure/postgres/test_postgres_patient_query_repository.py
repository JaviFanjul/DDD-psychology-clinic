from core.domain.model.patient.patient_query_repository import PatientDto
from core.infrastructure.postgres.postgres_patient_command_repository import (
    PostgresPatientCommandRepository,
)
from core.infrastructure.postgres.postgres_patient_query_repository import (
    PostgresPatientQueryRepository,
)


async def find_by_id(sessions, id):
    async with sessions() as session:
        return await PostgresPatientQueryRepository(session=session).find_by_id(id=id)


async def test_given_a_saved_patient_when_finding_it_then_it_returns_its_dto(sessions, patient):
    async with sessions() as session:
        await PostgresPatientCommandRepository(session=session).save(patient=patient)

    found = await find_by_id(sessions=sessions, id=patient.id)

    assert found == PatientDto(
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


async def test_given_no_patient_with_that_id_when_finding_it_then_it_returns_none(
    sessions, unknown_id
):
    found = await find_by_id(sessions=sessions, id=unknown_id)

    assert found is None
