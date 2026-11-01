from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class DomainEvent:
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
