from core.infrastructure.postgres.postgres_patient_command_repository import (
    PostgresPatientCommandRepository,
)
from core.infrastructure.postgres.postgres_unit_of_work import PostgresUnitOfWork


async def find_by_id(sessions, id):
    async with sessions() as session:
        return await PostgresPatientCommandRepository(session=session).find_by_id(id=id)


async def test_given_a_committed_unit_of_work_when_finding_from_another_session_then_it_is_found(sessions, patient):
    async with sessions() as session, PostgresUnitOfWork(session=session) as unit_of_work:
        await PostgresPatientCommandRepository(session=session).save(patient=patient)
        await unit_of_work.commit()

    assert await find_by_id(sessions=sessions, id=patient.id) is not None


async def test_given_an_uncommitted_unit_of_work_when_finding_from_another_session_then_it_is_not_found(
    sessions, patient
):
    async with sessions() as session, PostgresUnitOfWork(session=session):
        await PostgresPatientCommandRepository(session=session).save(patient=patient)

    assert await find_by_id(sessions=sessions, id=patient.id) is None
