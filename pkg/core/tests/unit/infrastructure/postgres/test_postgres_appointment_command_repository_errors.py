import pytest
from core.domain.model.appointment.errors import (
    AppointmentNotLoaded,
    AppointmentNotSaved,
    PatientAppointmentsNotLoaded,
)
from core.infrastructure.postgres.postgres_appointment_command_repository import (
    PostgresAppointmentCommandRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_saving_then_it_rolls_back_and_raises_not_saved(
    failing_session, appointment
):
    repository = PostgresAppointmentCommandRepository(session=failing_session)

    with pytest.raises(AppointmentNotSaved) as raised:
        await repository.save(appointment=appointment)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
    assert failing_session.rolled_back


async def test_given_a_failing_database_when_finding_then_it_raises_appointment_not_loaded(
    failing_session, appointment
):
    repository = PostgresAppointmentCommandRepository(session=failing_session)

    with pytest.raises(AppointmentNotLoaded) as raised:
        await repository.find_by_id(id=appointment.id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)


async def test_given_a_failing_database_when_finding_pending_by_patient_then_it_raises(failing_session, appointment):
    repository = PostgresAppointmentCommandRepository(session=failing_session)

    with pytest.raises(PatientAppointmentsNotLoaded) as raised:
        await repository.find_pending_by_patient(patient_id=appointment.patient_id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
