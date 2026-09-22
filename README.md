# SpecKit Greenfield Governance

This add-on distributes the policy in
[`docs/greenfield-governance-policy.md`](docs/greenfield-governance-policy.md)
through native SpecKit components.

- `workflow/workflow.yml` is the standalone `greenfield-bootstrap` Workflow.
- `preset/` is the thin `greenfield-governance` Preset for `specify`,
  `clarify`, `plan`, and `converge`.
- `bundle.yml` composes that Workflow and Preset with the existing
  `feature-governance` Preset and `feature-governance-guard` Extension.

The Bundle owns only installable components. Canonical PRD,
`architecture/baseline.md`, `ROADMAP.md`, the Constitution, and `specs/**` are
project-owned and are not bundle assets.

MVP Governance remains an independently installed governance layer and is not
distributed or owned by this Bundle.

## Conditional UX/UI lifecycle

UX/UI governance applies only to a Feature that materially changes a
user-facing surface or interaction; touching frontend code alone does not
trigger it. Before technical planning, the Feature asks whether it requires a
new UX decision. An established pattern is identified and reused without
shaping; otherwise the `speckit.plan` addendum instructs the agent to use the
installed Impeccable shape capability, bounded to the current Feature and
affected surfaces. If the capability is unavailable or cannot run, planning
stops and reports the missing capability rather than substituting generic UX
reasoning.
Availability is implicit in that named-capability invocation; the overlay adds
no custom availability detection.

If shaping changes user-observable Feature behavior, `spec.md` must be
reconciled and revalidated before planning continues. Presentation-only choices
do not belong in `spec.md`. During convergence, materially implemented UI needs
current rendered evidence in the target runtime. The `speckit.converge`
addendum instructs the agent to use the installed Impeccable critique capability
for UX or interaction risk and/or the installed Impeccable audit capability for
accessibility, responsiveness, theming, performance, or implementation-integrity
risk. Material findings or an unavailable required capability block convergence.
For browser-based surfaces, rendered browser evidence satisfies the target-runtime
evidence requirement.

Impeccable must be exposed as an installed Codex skill. Its review snapshots
are evidence, not governance authority. Artifact creation is YAGNI: `DESIGN.md`
is needed only for a concrete reusable UX/UI rule, surface artifacts only for
durable surface-local presentation decisions without a better authority, and no
UX review report is required. This overlay adds no UX/UI extension, hook,
workflow, command, aggregator, or mandatory artifact type.

## Component resolution and publication

SpecKit 0.16.2 resolves Bundle component IDs through native primitive catalogs
or already-installed components; `bundle.yml` deliberately does not contain
relative paths or a custom installer. Publishing requires immutable GitHub
release artifacts and matching native catalog entries for the Workflow,
Greenfield Preset, Feature Governance Preset, and Feature Governance Extension,
then a Bundle release artifact and bundle-catalog entry.
