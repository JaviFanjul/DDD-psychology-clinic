import pytest
from core.application.command.schedule_appointment import ScheduleAppointmentCommand
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.appointment_modality import AppointmentModality
from core.domain.model.appointment.appointment_status import AppointmentStatus
from core.domain.model.appointment.errors import AppointmentOverlaps
from core.domain.model.appointment.events import AppointmentScheduled
from core.domain.model.patient.errors import PatientNotActive, PatientNotFound
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.psychologist.errors import PsychologistNotFound
from core.domain.model.psychologist.psychologist_id import PsychologistId


def command_for(patient_id, psychologist_id, slot):
    return ScheduleAppointmentCommand(
        id=AppointmentId.generate(),
        patient_id=patient_id,
        psychologist_id=psychologist_id,
        slot=slot,
        modality=AppointmentModality.ONLINE,
    )


@pytest.fixture
def command(active_patient_dto, psychologist_dto, slot) -> ScheduleAppointmentCommand:
    return command_for(
        patient_id=PatientId.from_string(id=active_patient_dto.id),
        psychologist_id=PsychologistId.from_string(id=psychologist_dto.id),
        slot=slot,
    )


async def test_given_an_active_patient_and_a_free_agenda_when_handling_then_it_is_saved_pending(
    schedule_appointment_handler, appointment_repository, command
):
    await schedule_appointment_handler.handle(command=command)

    [appointment] = appointment_repository.saved
    assert appointment.id == command.id
    assert appointment.patient_id == command.patient_id
    assert appointment.psychologist_id == command.psychologist_id
    assert appointment.slot == command.slot
    assert appointment.modality is command.modality
    assert appointment.status is AppointmentStatus.PENDING


async def test_given_an_active_patient_and_a_free_agenda_when_handling_then_it_publishes_it(
    schedule_appointment_handler, event_bus, command
):
    await schedule_appointment_handler.handle(command=command)

    [event] = event_bus.published
    assert isinstance(event, AppointmentScheduled)
    assert event.appointment_id == command.id


async def test_given_a_command_when_handling_then_it_checks_the_psychologist_agenda_for_the_slot(
    schedule_appointment_handler, free_agenda, command
):
    await schedule_appointment_handler.handle(command=command)

    assert free_agenda.slot_queries == [(command.psychologist_id, command.id)]


async def test_given_a_busy_agenda_when_handling_then_it_raises_and_saves_and_publishes_nothing(
    schedule_appointment_handler_with_busy_agenda, appointment_repository, event_bus, command
):
    with pytest.raises(AppointmentOverlaps):
        await schedule_appointment_handler_with_busy_agenda.handle(command=command)

    assert appointment_repository.saved == []
    assert event_bus.published == []


@pytest.mark.parametrize(
    ("patient", "psychologist", "expected_error"),
    [
        ("unknown", "known", PatientNotFound),
        ("discharged", "known", PatientNotActive),
        ("active", "unknown", PsychologistNotFound),
    ],
)
async def test_given_an_ineligible_attendee_when_handling_then_it_raises_and_saves_nothing(
    schedule_appointment_handler,
    appointment_repository,
    event_bus,
    active_patient_dto,
    discharged_patient_dto,
    psychologist_dto,
    slot,
    patient,
    psychologist,
    expected_error,
):
    patient_ids = {
        "unknown": PatientId.generate(),
        "discharged": PatientId.from_string(id=discharged_patient_dto.id),
        "active": PatientId.from_string(id=active_patient_dto.id),
    }
    psychologist_ids = {
        "unknown": PsychologistId.generate(),
        "known": PsychologistId.from_string(id=psychologist_dto.id),
    }

    with pytest.raises(expected_error):
        await schedule_appointment_handler.handle(
            command=command_for(
                patient_id=patient_ids[patient],
                psychologist_id=psychologist_ids[psychologist],
                slot=slot,
            )
        )

    assert appointment_repository.saved == []
    assert event_bus.published == []
