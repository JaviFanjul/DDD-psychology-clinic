# ADR-3: Domain validation

**Status:** Accepted

**Date:** 2026-11-01

## Context

Python doesn't enforce type hints at runtime: `PatientId("not-a-uuid")` runs even though the field is declared as `UUID`. In a statically typed language the compiler rejects that call, so nobody would write a check for it. In Python it is tempting to add `isinstance` checks to the domain to fill that gap, which mixes two concerns: whether a value has the right type, and whether it satisfies a rule of the domain.

## Decision

1. **Types:** the domain doesn't validate types. It trusts its type hints, so there are no `isinstance` checks on inputs and no tests that pass a value of the wrong type.
2. **Boundary:** infrastructure turns external input into the right types before calling the domain.
3. **Domain rules:** the domain does validate the rules of its values, such as the format of an email, and raises a `DomainError` subclass when they are broken.

## Consequences

- Value objects hold only domain rules, and a `DomainError` always means a broken rule, never a programming mistake.
- A value of the wrong type that reaches the domain is not rejected. It either fails with a generic error such as `AttributeError`, or is accepted silently, as in `PatientId("not-a-uuid")`.
- This decision relies on infrastructure being the only way in. CI runs no static type checker, so nothing catches a wrong type passed from inside the code before it runs.
