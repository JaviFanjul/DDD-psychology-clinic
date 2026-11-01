# ADR-8: Import layers

**Status:** Accepted

**Date:** 2026-11-01

## Context

We follow DDD and hexagonal architecture, so the domain can't depend on how it's used or stored. Python doesn't stop a module from importing any other, and a wrong import works without any error, so reviews are the only thing that catches it. We need a rule that a machine can check. Neither uv nor mypy checks this, and ruff can only ban imports per folder through a nested config file, which would also end up in the package we build.

## Decision

1. **Tool:** we use the `layers` contract from `import-linter`, configured in the root `pyproject.toml`.
2. **Layers:** from top to bottom, `entrypoint | infrastructure`, `application` and `domain`. A layer can only import the layers below it.
3. **Adapters:** `entrypoint` and `infrastructure` share a level, separated by `|`, so neither can import the other. A controller reaches infrastructure through the interfaces in `domain`.
4. **Allowed imports:**

   | Layer | Can import |
   |---|---|
   | `domain` | nothing from the other layers |
   | `application` | `domain` |
   | `infrastructure` | `application`, `domain` |
   | `entrypoint` | `application`, `domain` |

5. **Scope:** this applies to the code in `src/`. Tests can import from any layer.
6. **CI:** the `architecture` job runs `lint-imports` and fails if the contract is broken.

## Consequences

- A wrong import fails CI, including imports inside a function and indirect ones that go through another module.
- The code that connects infrastructure to entrypoints can't live in either of them, so it has to go outside the four layers.
- The contract only covers imports between our layers. Nothing yet stops `domain` from importing a framework or a standard library module such as `sqlite3`, and there are no third-party dependencies to ban today.
- Adding a new top-level folder under `core` doesn't fail CI, so it has to be added to the contract by hand.
