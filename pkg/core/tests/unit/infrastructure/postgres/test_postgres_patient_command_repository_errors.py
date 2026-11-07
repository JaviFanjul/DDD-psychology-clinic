import pytest
from core.domain.model.patient.errors import PatientNotLoaded, PatientNotSaved
from core.infrastructure.postgres.postgres_patient_command_repository import (
    PostgresPatientCommandRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_saving_then_it_raises_not_saved(failing_session, patient):
    repository = PostgresPatientCommandRepository(session=failing_session)

    with pytest.raises(PatientNotSaved) as raised:
        await repository.save(patient=patient)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)


async def test_given_a_failing_database_when_finding_then_it_raises_patient_not_loaded(failing_session, patient):
    repository = PostgresPatientCommandRepository(session=failing_session)

    with pytest.raises(PatientNotLoaded) as raised:
        await repository.find_by_id(id=patient.id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
