# ADR-2: Pinned versions

**Status:** Accepted

**Date:** 2026-10-31

## Context

Builds and checks must be reproducible: the same commit has to give the same result on any machine and at any time.

## Decision

1. **Versions:** we always pin exact versions, instead of using ranges or floating references. This covers dependencies (`pytest==9.2.0`), the build backend (`uv_build==0.11.29`), Python (`==3.14.4`) and CI actions (`actions/checkout@v7.0.1`).
2. **Lock file:** `uv.lock` is committed, and CI runs every command with `--locked`, so it fails if the lock file is out of date instead of resolving new versions.

## Consequences

- CI and local environments use the same versions, including transitive dependencies.
- Upgrading a version is an explicit change, made in its own commit and reviewable in a diff.
- Changing a dependency requires updating `uv.lock` in the same change, or CI fails.
