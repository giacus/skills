# Review test evidence

Apply this to affected tests during ordinary change review. Review the whole
suite only when the user's specification asks for it; then reconcile all runner
profiles, nested/parameterized cases and script checks with the review record.

Read the test body, relevant setup/helpers and the code boundary it invokes.
Ask what concrete defect could occur, which assertion would fail, and why the
expected value is independently justified. A named scenario, assertion count or
green result does not answer those questions.

Check for:

- assertions satisfied entirely by setup or a mock, without exercising the
  claimed production boundary;
- expected values computed by the same potentially faulty production logic;
- vacuous empty collections, absent positive controls, unawaited work, and
  negative tests that fail in setup or at the wrong guard;
- harmful expectations that freeze incidental implementation, prose or timing,
  or reject supported behavior;
- duplication that adds no distinct defect detection, trust boundary or useful
  diagnosis; and test helpers that conceal weakened assertions.

Mocks are appropriate at real boundaries. Input-derived expected sets can
independently verify a transformation. Metamorphic and equivalence tests can
prove invariance without proving complete correctness; identify that narrower
role instead of automatically calling them tautologies. Exact bytes or text can
be the contract for reviewed assets, serialization and explicit package policy.

For removals and rewrites, check the exact retained protection and whether the
replacement passed against unchanged implementation. For high-risk changes,
look for a safe realistic fault that fails the intended assertion rather than
compilation or setup. Never infer equivalent protection from fewer green tests.

For an exhaustive request, every test needs a case-specific decision. Equivalent
parameter cases may share reasoning if all cases remain traceable. Challenge
retained tests too; a blanket KEEP row for a file or subsystem is insufficient.
Verify that known weak checks were resolved or honestly retained as uncertain.
Do not promote a few spot checks into a claim that every case was reviewed.

Keep case-specific decisions with the task or PR, bound to the reviewed revision.
Review depth does not depend on a new tracked Markdown or JSON report. Verify
that evidence is accessible and traceable; when a report leaves the active tree,
check its immutable recovery reference. Preserve independent oracles and
unresolved failure evidence, and promote lasting test contracts into existing
guidance rather than making historical ledgers required onboarding.
