# ADR-4: Domain events

**Status:** Accepted

**Date:** 2026-11-01

## Context

Domain events record what happens in the domain, and we need a shared criterion for defining them, so that they stay consistent as we add more.

## Decision

1. **Immutable:** an event can't change once created, because what has already happened can't change either. We declare them with `@dataclass(frozen=True)`.
2. **Past tense:** an event's name states something that has already happened, such as `PatientCreated`.
3. **Minimal data:** an event contains only the information that is essential to fulfil its purpose. `PatientCreated` carries the `PatientId`, not the whole patient.

## Consequences

- Whoever receives an event can trust that its data hasn't changed since it was created.
- An event's name tells what happened without having to read its code.
- Whoever needs more data than an event carries has to get it from somewhere else.
- Adding a field to an event requires justifying why its purpose can't be fulfilled without it.
