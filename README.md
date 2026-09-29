# SpecKit Greenfield Governance

This add-on distributes the policy in
[`docs/greenfield-governance-policy.md`](docs/greenfield-governance-policy.md)
through native SpecKit components.

- `workflow/` is the `greenfield-bootstrap` Workflow package, including its
  run-local PRD governance validator. Initial ROADMAP readiness requires the
  Greenfield lifecycle Extension installed by the Bundle.
- `preset/` is the thin `greenfield-governance` Preset for `specify`,
  `clarify`, `plan`, `tasks`, `implement`, and `converge`.
- `extension/` owns the ROADMAP status evaluator and one mandatory
  `after_converge` hook.
- `bundle.yml` composes those components with the existing
  `feature-governance` Preset and `feature-governance-guard` Extension.

The Bundle owns only installable components. Canonical PRD,
`architecture/baseline.md`, `ROADMAP.md`, the Constitution, and `specs/**` are
project-owned and are not bundle assets.

MVP Governance remains an independently installed governance layer and is not
distributed or owned by this Bundle.

## ROADMAP lifecycle

Greenfield Governance applies `planned → ready` after the final Greenfield
Bootstrap PROJECT READY gate approves the published ROADMAP,
`ready → active` after successful `speckit.specify`, and `active → done` after
clean, compatible `speckit.converge` plus fresh Feature Governance and MVP
Governance checks, complete tasks, and required verification. It then
reassesses direct dependents. `done` means governed Feature completion; product
release is separate. MVP Governance must be installed for completion. Existing
Feature and MVP hooks are unchanged, and routine status transitions need no
approval.

Each actionable ROADMAP entry needs the following lifecycle fields; normal
dependencies require the predecessor to be `done`. Include `Start requires`
only when the ROADMAP explicitly requires an extra file-based condition.

```md
<!-- roadmap-entry: RM-01 -->
### RM-01: Establish the service contract
Status: planned
Status reason: awaiting PROJECT READY
Depends on: none
Feature spec: none

<!-- roadmap-entry: RM-02 -->
### RM-02: Use the service contract
Status: planned
Status reason: waiting for RM-01
Depends on: RM-01
Feature spec: none
Start requires: file:contracts/service-v1.md
```

The status evaluator writes only lifecycle fields. Missing or ambiguous
evidence leaves status unchanged and reports the blocker. The post-converge
hook reruns the installed guards against current artifacts; it does not claim
to retain historical guard results.

## PRD convergence in bootstrap

`greenfield-bootstrap` records each full PRD review as structured run-local
state bound to the SHA-256 of the current Canonical PRD. A material `PRODUCT
GAP` stays unresolved through repeated reviews of unchanged content. Resume
the same run with a self-contained `prd_decision` and optional `prd_comment`;
bootstrap applies that decision to the Canonical PRD and reviews the new
revision. The validator suppresses replayed decisions and requires a real PRD
change plus a clean review to resolve the selected gap. Architecture begins
only when the latest review is clean, no gap remains unresolved, and explicit
approval is bound to that exact revision. Run-local JSON retains review,
resolution, and approval evidence; the human gate shows only the decision.

## Conditional UX/UI lifecycle

UX/UI governance applies only to a Feature that materially changes a
user-facing surface or interaction; touching frontend code alone does not
trigger it. Before technical planning, the Feature asks whether it requires a
new UX decision. An established pattern is identified and reused without
shaping only when `plan.md` names the exact reusable pattern, its authoritative
source, and why it fully determines the affected states and interactions.
Generic pattern references do not cover newly introduced states, commands,
destructive actions, hierarchy, or control composition. Otherwise the
`speckit.plan` addendum instructs the agent to use the installed Impeccable
shape capability, bounded to the current Feature and
affected surfaces. If the capability is unavailable or cannot run, planning
stops and reports the missing capability rather than substituting generic UX
reasoning.
Availability is implicit in that named-capability invocation; the overlay adds
no custom availability detection.

If shaping changes user-observable Feature behavior, `spec.md` must be
reconciled and revalidated before planning continues. Presentation-only choices
do not belong in `spec.md`. When the change needs new interaction decisions,
shaping records them in `specs/<feature>/ux-design.md` before technical planning.
The Feature-local artifact defines the affected surfaces, states, hierarchy,
actions and grouping, disclosure, controls, meaningful labels, transitions,
error/status presentation, accessibility and keyboard behavior, responsive
constraints, and acceptance-relevant rendered states as applicable. It must be
concrete enough for implementation to follow without inventing UX. No UX
artifact is required for a backend/non-UI Feature or a material UI change fully
determined by the cited established pattern.

At `speckit.tasks`, the Feature design or exact pattern recorded by Plan becomes
task input. Tasks retain concrete interaction decisions and include verification
or evidence work for acceptance-relevant rendered states. If a material change
needs `ux-design.md` and it is missing, Tasks stops and returns to Plan/UX
shaping. At `speckit.implement`, implementation reads the applicable `DESIGN.md`
and Feature design or recorded pattern directly; `tasks.md` cannot replace that
authority. Technical choices may vary within the approved interaction design.
Missing design authority or a newly discovered UX decision stops affected
implementation and returns the Feature to Plan/UX shaping. A capability list
alone does not authorize a control model or management UI layout.

During convergence, materially implemented UI needs current rendered evidence
in the target runtime. When `ux-design.md` applies, that evidence must cover its
affected user-facing states and rendered Impeccable critique is mandatory. It
checks conformance to `ux-design.md` and applicable `DESIGN.md` rules, plus the
rendered interaction and visual hierarchy. Without `ux-design.md`, critique
remains risk-based. Impeccable audit remains risk-based in either case. A
material critique finding blocks Converge until the affected UI is corrected,
the rendered state is rechecked, and critique is rerun. If the approved
`ux-design.md` itself needs revision, Converge returns to Plan/UX shaping.
An unavailable required capability blocks Converge. For browser-based surfaces,
rendered browser evidence satisfies the target-runtime evidence requirement.

Impeccable must be exposed as an installed Codex skill. Its review snapshots
are evidence, not governance authority. `DESIGN.md` owns reusable project-wide,
cross-Feature UX/UI rules only; it is not mandatory for every UI Feature.
`specs/<feature>/ux-design.md` owns concrete Feature-local interaction design
when new UX decisions are required. Optional surface artifacts hold durable
surface-local presentation details without a better authority and cannot replace
required Feature-local design. No UX review report is required. This overlay
adds no UX/UI extension, hook, workflow, command, or aggregator.

## Installation from GitHub

The commands below apply after the proposed `v0.6.0` source tag is published.
This installs the published source tags into a clean SpecKit 0.16.2 project
without archives, GitHub Releases, or catalogs. It uses native local/dev
component installation and then registers the local Bundle against the five
already-installed component IDs.

```bash
specify --version # expected: specify 0.16.2

mkdir -p ~/src/speckit-governance
cd ~/src/speckit-governance
git clone --branch v1.0.1 --depth 1 https://github.com/ahhakopian/speckit-feature-governance.git
git clone --branch v0.6.0 --depth 1 https://github.com/ahhakopian/speckit-greenfield-governance.git

mkdir -p ~/projects/greenfield-project
cd ~/projects/greenfield-project
specify init --here --integration codex --ignore-agent-tools

specify extension add --dev ~/src/speckit-governance/speckit-feature-governance/extension --priority 10
specify extension add --dev ~/src/speckit-governance/speckit-greenfield-governance/extension --priority 20
specify preset add --dev ~/src/speckit-governance/speckit-feature-governance/preset --priority 10
specify workflow add --dev ~/src/speckit-governance/speckit-greenfield-governance/workflow
specify preset add --dev ~/src/speckit-governance/speckit-greenfield-governance/preset --priority 20

specify bundle install ~/src/speckit-governance/speckit-greenfield-governance --offline

specify preset list
specify extension list
specify workflow list
specify bundle list
```

`specify bundle install` records `speckit-greenfield-governance@0.6.0`; because
the five components are installed first, it resolves them locally and adds no
catalog dependency.

## Component resolution and publication

SpecKit 0.16.2 resolves Bundle component IDs through native primitive catalogs
or already-installed components; `bundle.yml` deliberately does not contain
relative paths or a custom installer. Publishing requires immutable GitHub
release artifacts and matching native catalog entries for the Workflow,
Greenfield Preset, Greenfield Extension, Feature Governance Preset, and Feature Governance Extension,
then a Bundle release artifact and bundle-catalog entry.
