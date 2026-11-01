from dataclasses import dataclass
from datetime import UTC, datetime

from core.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class SomethingHappened(DomainEvent):
    payload: str


def test_given_no_created_at_when_creating_an_event_then_it_holds_the_current_utc_time():
    before = datetime.now(UTC)

    event = SomethingHappened(payload="a payload")

    after = datetime.now(UTC)
    assert before <= event.created_at <= after
    assert event.created_at.tzinfo is UTC
