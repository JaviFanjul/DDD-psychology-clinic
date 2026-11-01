# ADR-7: Named arguments

**Status:** Accepted

**Date:** 2026-11-01

## Context

Many of our signatures take several values of the same type, as in `PatientAddress(street, postal_code, city, province)`. When those values are passed by position, the type checker can't tell if two of them were swapped, and the call doesn't show which value is which. We need a shared criterion for how to call our own code.

## Decision

1. **Our code:** every call to a function, method or class defined in this repository names its arguments, such as `PatientAddress(street=street, postal_code=postal_code, city=city, province=province)`.
2. **One argument:** the rule also applies to calls with a single argument, such as `PatientEmail(value=email)`, so that nobody has to decide when it applies.
3. **Scope:** this applies to the code in `src/` and in tests.
4. **Other code:** calls to the standard library and to third-party libraries are out of scope, because some of their parameters can't be named, as in `len(values)`.

## Consequences

- A swapped argument can be seen at a glance, and reordering a signature doesn't silently change what a call means.
- Calls are longer, especially when the name of the argument repeats the name of the variable.
- Nothing enforces this yet, neither ruff nor mypy nor CI, so it depends on reviews to catch.
