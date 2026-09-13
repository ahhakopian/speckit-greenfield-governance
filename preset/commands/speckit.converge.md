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
