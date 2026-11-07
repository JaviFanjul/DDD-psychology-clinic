import pytest
from core.domain.model.appointment.psychologist_availability import PsychologistAvailability


@pytest.mark.parametrize(
    ("agenda", "expected"),
    [("free_agenda", True), ("agenda_without_conflicts", True), ("busy_agenda", False)],
)
async def test_given_an_agenda_when_asking_availability_then_it_is_free_unless_a_slot_overlaps(
    request, psychologist_id, appointment_id, slot, agenda, expected
):
    availability = PsychologistAvailability(repository=request.getfixturevalue(agenda))

    available = await availability.is_available(psychologist_id=psychologist_id, slot=slot, excluding=appointment_id)

    assert available is expected


async def test_given_a_slot_when_asking_availability_then_it_looks_at_that_psychologist_agenda(
    free_agenda, psychologist_id, appointment_id, slot
):
    availability = PsychologistAvailability(repository=free_agenda)

    await availability.is_available(psychologist_id=psychologist_id, slot=slot, excluding=appointment_id)

    assert free_agenda.slot_queries == [(psychologist_id, appointment_id)]
