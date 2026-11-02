import pytest
from core.domain.model.patient.errors import PatientNotLoaded
from core.infrastructure.postgres.postgres_patient_query_repository import (
    PostgresPatientQueryRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_finding_then_it_raises_patient_not_loaded(
    failing_session, patient
):
    repository = PostgresPatientQueryRepository(session=failing_session)

    with pytest.raises(PatientNotLoaded) as raised:
        await repository.find_by_id(id=patient.id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
