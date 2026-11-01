# ADR-5: CQRS repositories

**Status:** Accepted

**Date:** 2026-11-01

## Context

Changing an aggregate and answering a question about it need different things. A change needs the entity, with its rules and events, while an answer only needs data. A single repository would have to serve both, and we need a shared criterion for how each aggregate reads and writes, so that this stays consistent as we add more.

## Decision

1. **Two repositories:** each aggregate has one command repository and one query repository, such as `PatientCommandRepository` and `PatientQueryRepository`.
2. **Location:** both are `ABC` interfaces that live in the aggregate's folder, such as `domain/model/patient/`.
3. **Command repository:** it stores and loads the entity. It can read, as `find_by_id` does, but only so that a command can change what it loads, never to answer a caller.
4. **Query repository:** it returns DTOs such as `PatientDto`, never entities, so that a read can't change the aggregate or record events. DTOs live next to the query repository, never in the application layer.

## Consequences

- Each aggregate has two interfaces to maintain, and `find_by_id` can appear in both with different return types.
- A DTO has no behaviour, so a command can't use the query repository to load what it changes.
- This decision separates the interfaces, not the storage: it doesn't decide whether reads and writes use the same database.
