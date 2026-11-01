# ADR-9: Root dependencies

**Status:** Accepted

**Date:** 2026-11-01

## Context

The workspace will hold several packages under `pkg/`. If each one pins its own versions, the same library ends up pinned in several files, and upgrading it means going through all of them. We want one place for versions, while each package still says what it uses. uv already shares a single `uv.lock` across the workspace, but it has no version catalog, and it accepts a dependency in a member that isn't listed anywhere in the root.

## Decision

1. **Versions:** third-party versions used by the packages are pinned exactly once, in `constraint-dependencies` under `[tool.uv]` in the root `pyproject.toml`. This is where ADR-2's exact pins live for them.
2. **Members:** a workspace member lists the libraries it uses by name, without a version, such as `"sqlalchemy"` or `"psycopg[binary]"`. This covers `dependencies`, `optional-dependencies`, `dependency-groups` and `dev-dependencies`.
3. **Own sources:** a member can't declare a source for a third-party library. The only source it can use is `workspace = true`, to depend on another workspace member.
4. **Adding a library:** pin it in the root, list it in the member and run `uv lock`.
5. **Tools:** the tools in the root `dev` group keep their versions there, since no package depends on them.
6. **CI:** the `dependencies` job runs `check-member-dependencies`, from the `ci-scripts` workspace member, which follows the same `src/` and `tests/` layout as any other package. It reads the members from the root `pyproject.toml` and fails if one lists a library not pinned exactly in the root, declares a version or declares its own source.

## Consequences

- Every version is defined and upgraded in one file, and all packages share the versions in `uv.lock`.
- Each package installs only what it lists, and its wheel lists those dependencies.
- A wheel lists them without versions, so outside this workspace nothing fixes them. Only `uv.lock` guarantees the exact versions.
- Adding a library takes two edits instead of one.
- A pin in the root installs nothing by itself, so a pin that no package uses any more stays there until someone removes it.
- The check doesn't look at what the code imports. A library imported in `src/` but not listed in its package still has to be caught by the `types` and `tests` jobs.
