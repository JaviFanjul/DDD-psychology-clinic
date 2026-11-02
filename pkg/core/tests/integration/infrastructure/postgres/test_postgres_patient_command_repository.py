from core.domain.model.patient.patient_status import PatientStatus
from core.infrastructure.postgres.postgres_patient_command_repository import (
    PostgresPatientCommandRepository,
)


async def save(sessions, patient):
    async with sessions() as session:
        await PostgresPatientCommandRepository(session=session).save(patient=patient)


async def find_by_id(sessions, id):
    async with sessions() as session:
        return await PostgresPatientCommandRepository(session=session).find_by_id(id=id)


async def test_given_a_saved_patient_when_finding_it_then_it_returns_it(sessions, patient):
    await save(sessions=sessions, patient=patient)

    found = await find_by_id(sessions=sessions, id=patient.id)

    assert found.id == patient.id
    assert found.email == patient.email
    assert found.name == patient.name
    assert found.phone == patient.phone
    assert found.address == patient.address
    assert found.status == patient.status


async def test_given_a_saved_patient_when_saving_it_discharged_then_it_returns_it_discharged(
    sessions, patient
):
    await save(sessions=sessions, patient=patient)
    patient.discharge()

    await save(sessions=sessions, patient=patient)

    found = await find_by_id(sessions=sessions, id=patient.id)
    assert found.status is PatientStatus.DISCHARGED


async def test_given_no_patient_with_that_id_when_finding_it_then_it_returns_none(
    sessions, unknown_id
):
    found = await find_by_id(sessions=sessions, id=unknown_id)

    assert found is None
