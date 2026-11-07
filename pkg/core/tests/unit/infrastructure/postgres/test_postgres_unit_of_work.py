import pytest
from core.domain.unit_of_work import UnitOfWorkNotCommitted
from core.infrastructure.postgres.postgres_unit_of_work import PostgresUnitOfWork
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_committing_then_it_raises_not_committed(failing_session):
    unit_of_work = PostgresUnitOfWork(session=failing_session)

    with pytest.raises(UnitOfWorkNotCommitted) as raised:
        await unit_of_work.commit()

    assert isinstance(raised.value.__cause__, SQLAlchemyError)


async def test_given_an_error_inside_the_unit_of_work_when_leaving_it_then_it_rolls_back(failing_session):
    with pytest.raises(RuntimeError):
        async with PostgresUnitOfWork(session=failing_session):
            raise RuntimeError

    assert failing_session.rolled_back
