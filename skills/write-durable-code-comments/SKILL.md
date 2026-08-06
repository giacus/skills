---
name: write-durable-code-comments
description: >
  Experimentally write or update durable comments during implementation when a
  tempting local simplification could violate a verified, otherwise invisible
  invariant. Use for non-obvious ordering, lifecycle, concurrency, protocol,
  compatibility, trust, or domain constraints. Skip mechanical changes and
  standalone comment audits.
---

<!-- Independently authored. Inspired by
https://antirez.com/news/124 -->

# Write Durable Code Comments

Treat each warranted comment as an experimental handoff to a future maintainer.

## Workflow

1. Identify a verified local decision that a reasonable maintainer could undo
   because its constraint is invisible.
2. Prefer clearer code, types, assertions, or tests. Put cross-cutting decisions
   in repository guidance or a design document.
3. If the constraint remains hidden, write the smallest adjacent comment that
   states the constraint and the consequence of violating it. State rationale
   only when supported by verified evidence.
4. Update affected comments and validate the final behavior.

## Guardrails

- Expect zero comments for most changes.
- Keep comments local, factual, timeless, and about the software.
- Do not narrate code, preserve old implementations, invent rationale, add
  unowned debt notes, or duplicate tests and documentation.
- Never substitute comments for executable validation or structural separation.
- Fix or surface behavioral gaps; never comment as if an unsatisfied invariant
  holds.

## Review Gate

After implementation and tests, remove each proposed comment unless its claim is
verified, locally useful, and not cheaply recoverable. Report retained comments
as experimental proposals for review.

Prefer:

```text
Require two matching layout samples; one frame can capture a resize transition.
```

Over:

```text
Wait for layout.
```
