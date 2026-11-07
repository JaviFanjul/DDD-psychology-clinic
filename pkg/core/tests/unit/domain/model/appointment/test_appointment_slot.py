from datetime import UTC, datetime, timedelta, timezone

import pytest
from core.domain.model.appointment.appointment_slot import AppointmentSlot
from core.domain.model.appointment.errors import InvalidAppointmentSlot

STARTS_AT = datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC)


@pytest.mark.parametrize(
    ("starts_at", "duration_minutes"),
    [
        (datetime(year=2026, month=11, day=10, hour=9), 50),
        (STARTS_AT, 0),
        (STARTS_AT, -30),
    ],
)
def test_given_an_invalid_slot_when_creating_then_it_raises_invalid_appointment_slot(starts_at, duration_minutes):
    with pytest.raises(InvalidAppointmentSlot):
        AppointmentSlot(starts_at=starts_at, duration_minutes=duration_minutes)


def test_given_a_start_in_another_timezone_when_creating_then_it_holds_it_in_utc():
    madrid_winter = timezone(timedelta(hours=1))

    slot = AppointmentSlot(
        starts_at=datetime(year=2026, month=11, day=10, hour=10, tzinfo=madrid_winter),
        duration_minutes=50,
    )

    assert slot.starts_at == STARTS_AT
    assert slot.starts_at.tzinfo is UTC


def test_given_a_slot_when_asking_its_end_then_it_adds_the_duration_to_the_start():
    slot = AppointmentSlot(starts_at=STARTS_AT, duration_minutes=50)

    ends_at = slot.ends_at

    assert ends_at == datetime(year=2026, month=11, day=10, hour=9, minute=50, tzinfo=UTC)


@pytest.mark.parametrize(
    ("start_hour", "start_minute", "duration_minutes", "expected"),
    [
        (9, 0, 50, True),
        (9, 30, 60, True),
        (8, 30, 60, True),
        (8, 0, 120, True),
        (9, 10, 10, True),
        (8, 0, 60, False),
        (9, 50, 50, False),
        (11, 0, 50, False),
    ],
)
def test_given_two_slots_when_checking_overlap_then_it_tells_whether_they_share_time(
    start_hour, start_minute, duration_minutes, expected
):
    slot = AppointmentSlot(starts_at=STARTS_AT, duration_minutes=50)
    other = AppointmentSlot(
        starts_at=STARTS_AT.replace(hour=start_hour, minute=start_minute),
        duration_minutes=duration_minutes,
    )

    assert slot.overlaps(other=other) is expected
    assert other.overlaps(other=slot) is expected
