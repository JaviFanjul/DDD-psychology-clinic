from datetime import UTC, datetime

from core.domain.model.appointment.appointment import Appointment
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.infrastructure.postgres.postgres_appointment_command_repository import (
    PostgresAppointmentCommandRepository,
)
from core.infrastructure.postgres.postgres_appointment_query_repository import (
    PostgresAppointmentQueryRepository,
)


async def save(sessions, appointment):
    async with sessions() as session:
        await PostgresAppointmentCommandRepository(session=session).save(appointment=appointment)


def another_appointment(appointment, status, starts_at_hour):
    return Appointment(
        id=AppointmentId.generate(),
        patient_id=appointment.patient_id,
        psychologist_id=appointment.psychologist_id,
        slot=AppointmentSlot(
            starts_at=datetime(year=2026, month=11, day=11, hour=starts_at_hour, tzinfo=UTC),
            duration_minutes=60,
        ),
        modality=AppointmentModality.IN_PERSON,
        status=status,
    )


async def test_given_a_saved_appointment_when_finding_it_then_it_returns_its_dto(
    sessions, appointment
):
    await save(sessions=sessions, appointment=appointment)

    async with sessions() as session:
        found = await PostgresAppointmentQueryRepository(session=session).find_by_id(
            id=appointment.id
        )

    assert found == AppointmentDto(
        id="3f2504e0-4f89-41d3-9a0c-0305e82c3301",
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        psychologist_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC),
        duration_minutes=50,
        modality="online",
        status="pending",
    )


async def test_given_a_changed_appointment_when_saving_and_loading_it_then_it_keeps_the_changes(
    sessions, appointment
):
    await save(sessions=sessions, appointment=appointment)
    new_slot = AppointmentSlot(
        starts_at=datetime(year=2026, month=11, day=12, hour=16, tzinfo=UTC), duration_minutes=60
    )
    appointment.reschedule(slot=new_slot)
    appointment.cancel()
    await save(sessions=sessions, appointment=appointment)

    async with sessions() as session:
        found = await PostgresAppointmentCommandRepository(session=session).find_by_id(
            id=appointment.id
        )

    assert found.slot == new_slot
    assert found.status is AppointmentStatus.CANCELLED
    assert found.pull_events() == []


async def test_given_no_appointment_with_that_id_when_finding_it_then_both_repositories_say_none(
    sessions, unknown_appointment_id
):
    async with sessions() as session:
        from_query = await PostgresAppointmentQueryRepository(session=session).find_by_id(
            id=unknown_appointment_id
        )
        from_command = await PostgresAppointmentCommandRepository(session=session).find_by_id(
            id=unknown_appointment_id
        )

    assert from_query is None
    assert from_command is None


async def test_given_appointments_in_every_status_when_finding_pending_by_patient_then_only_pending(
    sessions, appointment
):
    cancelled = another_appointment(
        appointment=appointment, status=AppointmentStatus.CANCELLED, starts_at_hour=10
    )
    completed = another_appointment(
        appointment=appointment, status=AppointmentStatus.COMPLETED, starts_at_hour=12
    )
    for saved in (appointment, cancelled, completed):
        await save(sessions=sessions, appointment=saved)

    async with sessions() as session:
        found = await PostgresAppointmentCommandRepository(session=session).find_pending_by_patient(
            patient_id=appointment.patient_id
        )

    assert [pending.id for pending in found] == [appointment.id]


async def test_given_appointments_in_every_status_when_finding_pending_slots_then_only_pending(
    sessions, appointment, slot
):
    pending = another_appointment(
        appointment=appointment, status=AppointmentStatus.PENDING, starts_at_hour=10
    )
    cancelled = another_appointment(
        appointment=appointment, status=AppointmentStatus.CANCELLED, starts_at_hour=12
    )
    for saved in (appointment, pending, cancelled):
        await save(sessions=sessions, appointment=saved)

    async with sessions() as session:
        found = await PostgresAppointmentQueryRepository(session=session).find_pending_slots(
            psychologist_id=appointment.psychologist_id, excluding=AppointmentId.generate()
        )

    assert sorted(found, key=lambda found_slot: found_slot.starts_at) == [slot, pending.slot]


async def test_given_a_pending_appointment_when_finding_slots_excluding_it_then_it_is_left_out(
    sessions, appointment
):
    await save(sessions=sessions, appointment=appointment)

    async with sessions() as session:
        found = await PostgresAppointmentQueryRepository(session=session).find_pending_slots(
            psychologist_id=appointment.psychologist_id, excluding=appointment.id
        )

    assert found == []


async def test_given_a_pending_appointment_when_finding_another_psychologist_slots_then_none(
    sessions, appointment
):
    await save(sessions=sessions, appointment=appointment)

    async with sessions() as session:
        found = await PostgresAppointmentQueryRepository(session=session).find_pending_slots(
            psychologist_id=PsychologistId.generate(), excluding=AppointmentId.generate()
        )

    assert found == []
