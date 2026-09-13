## Greenfield Governance — Specify Addendum

Apply this addendum in addition to the core command. A Feature may be
specified only from a ready, unblocked `ROADMAP.md` entry. Identify that entry
in `spec.md` and keep the Feature within its outcome, scope boundary,
architecture responsibility, dependencies, and the approved
`architecture/baseline.md`.

Classify any material issue by the authority that must change, and stop rather
than resolving it in the Feature:

- New or changed product scope, capability, actor, authority, ownership, or
  product boundary: return it to the Canonical PRD.
- A material change to approved architecture: report
  `BASELINE_CHANGE_REQUIRED` and stop for Controlled Architecture Change.
- A change only to Feature decomposition, boundary, dependency, or ordering:
  escalate it to `ROADMAP.md`.

Only Feature-local detail that is consistent with all upstream authorities may
be added to `spec.md`.
