# ADR-6: Type hints on domain types

**Status:** Accepted

**Date:** 2026-11-01

## Context

Function signatures already declare their types, but a local variable doesn't show what it holds. When reading a controller or a handler, it matters whether a value is still a primitive or has already become a domain type, and we need a shared criterion so that this stays visible everywhere.

## Decision

1. **Domain types:** every local variable that holds a domain type declares it, not only function signatures, such as `patient_id: PatientId = PatientId.generate()`.
2. **What counts as a domain type:** anything defined in `domain/`, such as entities, value objects, events and DTOs, including collections and optionals of them, such as `list[DomainEvent]` and `PatientDto | None`.
3. **Primitives:** local variables holding primitives don't need a hint, such as `normalized` in `PatientEmail`.
4. **Scope:** this applies to the code in `src/`, not to tests.
5. **Loop variables:** they stay without a hint, because Python doesn't allow annotating them inline.
6. **Type checker:** mypy checks `src/` in strict mode, in the `types` CI job.

## Consequences

- The boundary between primitives and domain types can be seen at a glance.
- Some lines repeat the type, as in `patient_email: PatientEmail = PatientEmail(email)`.
- mypy rejects a hint that doesn't match the value, but it infers local types instead of requiring them, so leaving a hint out still depends on reviews to catch.
