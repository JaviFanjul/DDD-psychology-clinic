from datetime import UTC, datetime, timedelta, timezone

from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.infrastructure.postgres.appointment_mapper import AppointmentMapper


def test_given_an_appointment_when_mapping_to_model_then_it_flattens_its_value_objects(
    appointment, appointment_model
):
    mapped = AppointmentMapper.to_model(appointment=appointment)

    assert (
        mapped.id,
        mapped.patient_id,
        mapped.psychologist_id,
        mapped.starts_at,
        mapped.duration_minutes,
        mapped.modality,
        mapped.status,
    ) == (
        appointment_model.id,
        appointment_model.patient_id,
        appointment_model.psychologist_id,
        appointment_model.starts_at,
        appointment_model.duration_minutes,
        appointment_model.modality,
        appointment_model.status,
    )


def test_given_a_model_when_mapping_to_entity_then_it_rebuilds_the_appointment_without_events(
    appointment_model, appointment
):
    mapped = AppointmentMapper.to_entity(model=appointment_model)

    assert mapped.id == appointment.id
    assert mapped.patient_id == appointment.patient_id
    assert mapped.psychologist_id == appointment.psychologist_id
    assert mapped.slot == appointment.slot
    assert mapped.modality is appointment.modality
    assert mapped.status is AppointmentStatus.PENDING
    assert mapped.pull_events() == []


def test_given_a_model_when_mapping_to_dto_then_it_copies_its_columns_with_the_start_in_utc(
    appointment_model,
):
    appointment_model.starts_at = datetime(
        year=2026, month=11, day=10, hour=10, tzinfo=timezone(timedelta(hours=1))
    )

    mapped = AppointmentMapper.to_dto(model=appointment_model)

    assert mapped == AppointmentDto(
        id="3f2504e0-4f89-41d3-9a0c-0305e82c3301",
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        psychologist_id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC),
        duration_minutes=50,
        modality="online",
        status="pending",
    )
    assert mapped.starts_at.tzinfo is UTC


def test_given_a_cancelled_appointment_when_mapping_to_model_and_back_then_it_keeps_its_status(
    appointment,
):
    appointment.cancel()

    mapped = AppointmentMapper.to_entity(model=AppointmentMapper.to_model(appointment=appointment))

    assert mapped.status is AppointmentStatus.CANCELLED
