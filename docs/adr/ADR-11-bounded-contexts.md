# ADR-11: Bounded contexts

**Status:** Accepted

**Date:** 2026-11-06

## Context

So far all the code lives in `core`, which models the clinic's patients. We're going to add an AI assistant, which speaks a different language, such as conversations, messages, prompts and tools, changes for different reasons, such as a new LLM or new prompts, and needs libraries that `core` doesn't use. If we put it inside `core`, both languages get mixed, and `core` ends up depending on everything the assistant needs. We need a criterion for where a new part of the system goes and how it talks to the rest.

## Decision

1. **One package per bounded context:** each bounded context is a workspace member under `pkg/`, with the same `src/` and `tests/` layout and the same layers as `core`. The assistant goes in `pkg/assistant`.
2. **Layers:** each context has its own `layers` contract from ADR-8.
3. **Independence:** contexts can't import each other. An `independence` contract from `import-linter` covers every package under `pkg/`, and the `architecture` job fails if one imports another.
4. **Communication:** a context only knows another one through what it publishes, such as its HTTP API or its events in RabbitMQ.
5. **Anti-corruption layer:** a context that needs another one defines a port in its own `domain`, with its own types, such as a `PatientDirectory` in the assistant. Its `infrastructure` implements it by talking to the other context and translating its data, so the other context's model never reaches its domain.
6. **Dependencies:** each context lists only the libraries it uses, following ADR-9.
7. **Building blocks:** each context defines its own base classes, such as `DomainEvent` and `DomainError`, and only the ones it uses. We'll extract them into a shared package only when keeping them duplicated becomes a real cost.

## Consequences

- Each context has its own language, and a change in one doesn't force a change in another unless it changes what it publishes.
- `core` doesn't install the assistant's libraries, nor the other way round.
- Reusing code from another context isn't possible, so shared ideas, such as a patient's id, get their own type in each context.
- Building blocks such as `DomainEvent` and `DomainError` are duplicated in each context, and a change to one of them has to be repeated by hand in the others.
- Talking through HTTP or events is slower and can fail in ways an import can't, so each anti-corruption layer has to handle those errors.
- Adding a context means adding it to the `import-linter` contracts and the `mypy` paths in the root `pyproject.toml` by hand.
