# ADR-10: Aggregate encapsulation

**Status:** Accepted

**Date:** 2026-11-02

## Context

An aggregate guards its rules and records its events in the methods that change it, such as `Patient.discharge`. Python doesn't have private attributes, so if an aggregate's state is a public attribute, anyone can assign it, as in `patient.status = PatientStatus.DISCHARGED`, skipping both the rule and the event. We need a shared criterion for how aggregates expose and change their state, so that this stays consistent as we add more.

## Decision

1. **Private state:** an aggregate keeps its state in attributes prefixed with `_`, such as `_status`.
2. **Read-only properties:** it exposes the state that others need to read through properties without a setter, such as `status`.
3. **Business methods:** its state only changes through methods named after what happens in the domain, such as `discharge` and `readmit`, never through setters. Each method guards its rules and records its events.
4. **Only what a use case needs:** an aggregate gets a method to change something only when a use case needs it. `Patient` has no method to change its email until a use case changes it, and then it gets one such as `change_email`, not `set_email`.
5. **Creation and reconstitution:** a classmethod such as `Patient.create` is the only way an aggregate is born, with its initial state and its creation event. The constructor only rebuilds an aggregate that already exists, such as from storage, and records no events.
6. **Identity:** an aggregate defines `__eq__` and `__hash__` by its id, because it is the same aggregate whatever its data. Value objects, on the other hand, compare by value.

## Consequences

- Breaking an aggregate's rules from outside requires touching an attribute prefixed with `_`, which signals in review that something is wrong.
- Assigning a property fails mypy, which runs in CI in strict mode, and raises `AttributeError` at runtime, so there are no tests for it.
- Tests can't put an aggregate into a given state by assigning it. They build it with the constructor or reach the state through its business methods.
- Each aggregate needs a property per field it exposes, which is more code than public attributes.
- Two instances of the same aggregate compare as equal even if one of them is stale, so `==` can't be used to check that two copies hold the same data.
