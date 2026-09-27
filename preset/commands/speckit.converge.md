## Greenfield Governance — Converge Addendum

Apply this addendum in addition to the core command. Perform the final
compatibility check across these three levels:

1. Feature-local artifacts and implementation;
2. the approved `architecture/baseline.md`;
3. the originating `ROADMAP.md` entry's architecture responsibility and
   dependencies.

Report the result of each level and whether the implementation preserves the
Canonical PRD. Report a final classification of `COMPATIBLE` or
`BASELINE_CHANGE_REQUIRED`.

Release may proceed only when all three levels pass, the Canonical PRD is
preserved, and the final classification is `COMPATIBLE`. A
`BASELINE_CHANGE_REQUIRED` result blocks release until Controlled Architecture
Change completes and the Feature reconverges. Route a product conflict to the
Canonical PRD rather than resolving it in convergence.

Also determine from both Feature intent and the actual implementation whether
user-facing UI was materially changed. For material UI, require current
rendered evidence in the target runtime for the affected flow or states and
representative viewport or device classes as appropriate. For browser-based
surfaces, rendered browser evidence satisfies this requirement. Evaluate only
against applicable authority: reconciled `spec.md`, relevant upstream product
constraints, applicable `DESIGN.md`, and applicable surface-specific decisions.
Do not turn this focused check into a full product re-audit.

Choose specialist review proportionately to actual risk:

- When UX or interaction quality is materially at risk, invoke: **Use the installed Impeccable critique capability for the affected Feature and surfaces.**
- When accessibility, responsiveness, theming, performance, or implementation
  integrity is materially at risk, invoke: **Use the installed Impeccable audit capability for the affected Feature and surfaces.**
- Invoke both only when both categories are materially at risk or the change is
  a substantial new or redesigned surface.

If a required named capability is unavailable or cannot run, stop convergence
and report the missing capability; do not perform availability detection or
substitute generic UX reasoning. Material findings block convergence until
resolved. After a material fix, reverify the affected behavior. Polish is
optional and finding-driven. Do not require a review artifact merely to prove
that review occurred. The UX/UI conditions must pass before returning the
existing final `COMPATIBLE` classification.

Report the native outcome (`converged` or `tasks_appended`) and exactly one
Greenfield classification (`COMPATIBLE` or `BASELINE_CHANGE_REQUIRED`). Do not
modify ROADMAP in this command: the Greenfield-owned mandatory hook evaluates
completion from current artifacts, its own current compatibility check, and
fresh installed governance reviews.
