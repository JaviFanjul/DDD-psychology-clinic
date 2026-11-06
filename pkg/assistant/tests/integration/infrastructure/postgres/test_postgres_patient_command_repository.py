from assistant.infrastructure.postgres.postgres_patient_command_repository import (
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
    assert found.is_active


async def test_given_a_saved_patient_when_saving_it_inactive_then_it_returns_it_inactive(
    sessions, patient
):
    await save(sessions=sessions, patient=patient)
    patient.deactivate()

    await save(sessions=sessions, patient=patient)

    found = await find_by_id(sessions=sessions, id=patient.id)
    assert not found.is_active


async def test_given_no_patient_with_that_id_when_finding_it_then_it_returns_none(
    sessions, unknown_patient_id
):
    found = await find_by_id(sessions=sessions, id=unknown_patient_id)

    assert found is None
