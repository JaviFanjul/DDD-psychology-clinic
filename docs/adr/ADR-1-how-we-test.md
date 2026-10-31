# ADR-1: How we test

**Status:** Accepted

**Date:** 2026-10-31

## Context

We need a shared criterion for writing tests, so that they stay consistent and don't grow beyond what they contribute.

## Decision

1. **Given/When/Then:** every test follows this structure.
2. **Parametrization:** parametrize whenever possible, instead of repeating tests that differ only in their data.
3. **Fixtures:** they live next to the tests that use them, in a `conftest.py`.
4. **Third-party libraries:** we don't test other libraries' code, only the behaviour owned by the code under test.

## Consequences

- All tests read the same way: starting situation, action and expected result.
- Adding a case to an already covered behaviour usually means adding a row to a parametrization.
- Fixtures are found in the same folder as their tests.
- What a library guarantees, such as `dataclass` equality, needs no test of its own.
