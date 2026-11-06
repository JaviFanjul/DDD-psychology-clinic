# ADR-12: Command results

**Status:** Accepted

**Date:** 2026-11-06

## Context

Following command-query separation, our commands change state and return nothing, and data is read through queries. When a patient talks to the assistant, the reply only exists once the command has run. Without returning it, the client has to send the message and then ask for the reply in a second request, or the reply has to be produced in the background, through a queue and a worker, and delivered to the client later. The first takes two requests for every message, and the second needs infrastructure we don't need yet.

## Decision

1. **Exception:** in the `assistant` context, `TalkToAssistantCommand` returns the assistant's reply. This is a deliberate exception to command-query separation, because the reply is the outcome of the operation itself, not a read of stored data.
2. **Typed result:** the assistant's `Command` and `CommandHandler` are generic in their result, as `Command[TResult]`, the same way as `Query[TResult]`. A command that returns nothing is a `Command[None]`.
3. **No reads:** a command never returns data that a query could answer, such as the whole conversation.
4. **Scope:** `core`'s commands still return nothing, following ADR-11.
5. **Way out:** if replies become too slow for a single request, `TalkToAssistantCommand` will return nothing, and a worker consuming a queue will ask the assistant and record its reply.

## Consequences

- Talking to the assistant takes a single request, and the reply returned is the one to the patient's own message.
- The building blocks of `core` and `assistant` differ, since only the assistant's `Command` is generic.
- Moving to the queue only changes the application and infrastructure layers, since the conversation records the patient's message and the assistant's reply through separate methods.
- Deciding whether something is the outcome of an operation or a read is a judgement call, so it depends on reviews to catch.
