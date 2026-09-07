---
name: focused-debugging
description: Diagnose difficult, unexplained, intermittent, or persistent bugs and performance regressions. Use for explicit systematic diagnosis or failures whose cause remains uncertain; handle obvious narrow fixes directly.
---

# Focused Debugging

Use the phases below as diagnostic tools. Choose and revisit them according to
the evidence; a simple, established cause does not require the full workflow.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

A representative failure signal helps distinguish causes and verify a fix. Source inspection, instrumentation, and reproduction can inform each other; none guarantees a diagnosis alone.

Invest in a useful failure signal, bounded by the task and available environment.

### Possible feedback loops

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", use bounded samples and retain failing inputs and seeds.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **Human-assisted reproduction.** If human interaction is necessary, capture clear steps and observations. `scripts/hitl-loop.template.sh` is an optional helper.

A representative feedback loop narrows the search and can later verify the fix.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

Improve speed and repeatability when the expected diagnostic benefit justifies the setup cost.

### Non-deterministic bugs

For intermittent failures, use bounded repeated trials and record reproduction frequency. Choose stress, timing controls, or instrumentation that discriminate causes without changing the reported bug. Do not promise a deterministic verdict or chase an arbitrary reproduction rate.

### When you genuinely cannot build a loop

State what cannot yet be reproduced and continue useful source inspection or analysis of available evidence. Keep hypotheses and unverified fixes explicitly provisional. Ask for missing environment access or redacted artifacts when they are necessary to proceed. Production instrumentation requires the appropriate explicit authorization.

### Evidence for a reproduction claim

Record the invocation or interaction and the observed failure, with sensitive
output redacted. The signal must exercise the reported bug and detect its specific
symptom. State remaining nondeterminism and environment limitations; a slow or
human-assisted reproduction can still provide useful evidence.

Read relevant source and form provisional hypotheses when needed to construct the reproduction. Do not treat an untested theory as a confirmed cause or report the bug reproduced without a matching observed failure.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

When reduction helps diagnosis, remove unrelated inputs, callers, configuration, or steps while checking that the same failure remains.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Stop minimizing when the scenario isolates the relevant mechanism and further reduction would not materially improve diagnosis.

Revisit reproduction or minimization when a hypothesis reveals a better way to isolate the failure.

## Phase 3: Hypothesise

Rank the plausible causes supported by current evidence. Consider alternatives when the cause is uncertain; do not invent a fixed number of hypotheses when one decisive observation identifies it.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it; proceed with your ranking if the user is AFK.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5: Fix + regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6: Cleanup

Required before declaring done:

- [ ] The original scenario is checked against the fix; reuse the Phase 5 result if nothing relevant changed, and state any remaining uncertainty
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message, so the next debugger learns
