import pytest
from core.domain.model.appointment.errors import (
    AppointmentNotLoaded,
    PsychologistAppointmentsNotLoaded,
)
from core.infrastructure.postgres.postgres_appointment_query_repository import (
    PostgresAppointmentQueryRepository,
)
from sqlalchemy.exc import SQLAlchemyError


async def test_given_a_failing_database_when_finding_then_it_raises_appointment_not_loaded(
    failing_session, appointment
):
    repository = PostgresAppointmentQueryRepository(session=failing_session)

    with pytest.raises(AppointmentNotLoaded) as raised:
        await repository.find_by_id(id=appointment.id)

    assert isinstance(raised.value.__cause__, SQLAlchemyError)


async def test_given_a_failing_database_when_finding_pending_slots_then_it_raises_not_loaded(
    failing_session, appointment
):
    repository = PostgresAppointmentQueryRepository(session=failing_session)

    with pytest.raises(PsychologistAppointmentsNotLoaded) as raised:
        await repository.find_pending_slots(
            psychologist_id=appointment.psychologist_id, excluding=appointment.id
        )

    assert isinstance(raised.value.__cause__, SQLAlchemyError)
