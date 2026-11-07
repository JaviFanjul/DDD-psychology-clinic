from datetime import datetime

import pytest
from core.application.appointment.command.cancel_appointment import CancelAppointmentCommand
from core.application.appointment.command.change_appointment_modality import (
    ChangeAppointmentModalityCommand,
)
from core.application.appointment.command.complete_appointment import CompleteAppointmentCommand
from core.application.appointment.command.reschedule_appointment import RescheduleAppointmentCommand
from core.application.appointment.command.schedule_appointment import ScheduleAppointmentCommand
from core.application.appointment.query.get_appointment import GetAppointmentQuery
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.errors import (
    InvalidAppointmentId,
    InvalidAppointmentModality,
    InvalidAppointmentSlot,
)
from core.domain.model.patient.errors import InvalidPatientId
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.errors import InvalidPsychologistId
from core.domain.model.psychologist.psychologist_id import PsychologistId

NAIVE_START = datetime(year=2026, month=11, day=10, hour=9)


async def test_given_valid_data_when_scheduling_then_it_dispatches_the_command_with_the_returned_id(
    controller, command_bus, schedule_data, starts_at
):
    id = await controller.schedule(**schedule_data)

    assert command_bus.handled == [
        ScheduleAppointmentCommand(
            id=AppointmentId.from_string(id=id),
            patient_id=PatientId.from_string(id="7c9e6679-7425-40de-944b-e07fc1f90ae7"),
            psychologist_id=PsychologistId.from_string(id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"),
            slot=AppointmentSlot(starts_at=starts_at, duration_minutes=50),
            modality=AppointmentModality.ONLINE,
        )
    ]


async def test_given_two_schedulings_when_scheduling_then_each_gets_its_own_id(
    controller, schedule_data
):
    first_id = await controller.schedule(**schedule_data)
    second_id = await controller.schedule(**schedule_data)

    assert first_id != second_id


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_error"),
    [
        ("patient_id", "not-a-uuid", InvalidPatientId),
        ("psychologist_id", "not-a-uuid", InvalidPsychologistId),
        ("starts_at", NAIVE_START, InvalidAppointmentSlot),
        ("duration_minutes", 0, InvalidAppointmentSlot),
        ("modality", "phone", InvalidAppointmentModality),
    ],
)
async def test_given_an_invalid_field_when_scheduling_then_it_raises_and_dispatches_nothing(
    controller, command_bus, schedule_data, field, invalid_value, expected_error
):
    with pytest.raises(expected_error):
        await controller.schedule(**{**schedule_data, field: invalid_value})

    assert command_bus.handled == []


async def test_given_an_id_when_getting_then_it_dispatches_the_query_and_returns_its_result(
    controller, query_bus, appointment_dto
):
    appointment = await controller.get(id=appointment_dto.id)

    assert query_bus.handled == [
        GetAppointmentQuery(id=AppointmentId.from_string(id=appointment_dto.id))
    ]
    assert appointment == appointment_dto


async def test_given_valid_data_when_rescheduling_then_it_dispatches_the_command(
    controller, command_bus, appointment_dto, starts_at
):
    await controller.reschedule(id=appointment_dto.id, starts_at=starts_at, duration_minutes=60)

    assert command_bus.handled == [
        RescheduleAppointmentCommand(
            id=AppointmentId.from_string(id=appointment_dto.id),
            slot=AppointmentSlot(starts_at=starts_at, duration_minutes=60),
        )
    ]


async def test_given_an_invalid_slot_when_rescheduling_then_it_raises_and_dispatches_nothing(
    controller, command_bus, appointment_dto
):
    with pytest.raises(InvalidAppointmentSlot):
        await controller.reschedule(
            id=appointment_dto.id, starts_at=NAIVE_START, duration_minutes=60
        )

    assert command_bus.handled == []


async def test_given_valid_data_when_changing_modality_then_it_dispatches_the_command(
    controller, command_bus, appointment_dto
):
    await controller.change_modality(id=appointment_dto.id, modality="in_person")

    assert command_bus.handled == [
        ChangeAppointmentModalityCommand(
            id=AppointmentId.from_string(id=appointment_dto.id),
            modality=AppointmentModality.IN_PERSON,
        )
    ]


async def test_given_an_unknown_modality_when_changing_it_then_it_raises_and_dispatches_nothing(
    controller, command_bus, appointment_dto
):
    with pytest.raises(InvalidAppointmentModality):
        await controller.change_modality(id=appointment_dto.id, modality="phone")

    assert command_bus.handled == []


@pytest.mark.parametrize(
    ("action", "command_type"),
    [("cancel", CancelAppointmentCommand), ("complete", CompleteAppointmentCommand)],
)
async def test_given_an_id_when_closing_then_it_dispatches_the_command(
    controller, command_bus, appointment_dto, action, command_type
):
    await getattr(controller, action)(id=appointment_dto.id)

    assert command_bus.handled == [
        command_type(id=AppointmentId.from_string(id=appointment_dto.id))
    ]


@pytest.mark.parametrize(
    "call",
    [
        lambda controller, starts_at: controller.get(id="not-a-uuid"),
        lambda controller, starts_at: controller.reschedule(
            id="not-a-uuid", starts_at=starts_at, duration_minutes=50
        ),
        lambda controller, starts_at: controller.change_modality(
            id="not-a-uuid", modality="online"
        ),
        lambda controller, starts_at: controller.cancel(id="not-a-uuid"),
        lambda controller, starts_at: controller.complete(id="not-a-uuid"),
    ],
    ids=["get", "reschedule", "change_modality", "cancel", "complete"],
)
async def test_given_a_malformed_id_when_calling_then_it_raises_and_dispatches_nothing(
    controller, command_bus, query_bus, starts_at, call
):
    with pytest.raises(InvalidAppointmentId):
        await call(controller, starts_at)

    assert command_bus.handled == []
    assert query_bus.handled == []
