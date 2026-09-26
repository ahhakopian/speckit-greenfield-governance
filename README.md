# SpecKit Greenfield Governance

This add-on distributes the policy in
[`docs/greenfield-governance-policy.md`](docs/greenfield-governance-policy.md)
through native SpecKit components.

- `workflow/` is the standalone `greenfield-bootstrap` Workflow package,
  including its run-local PRD governance validator.
- `preset/` is the thin `greenfield-governance` Preset for `specify`,
  `clarify`, `plan`, and `converge`.
- `bundle.yml` composes that Workflow and Preset with the existing
  `feature-governance` Preset and `feature-governance-guard` Extension.

The Bundle owns only installable components. Canonical PRD,
`architecture/baseline.md`, `ROADMAP.md`, the Constitution, and `specs/**` are
project-owned and are not bundle assets.

MVP Governance remains an independently installed governance layer and is not
distributed or owned by this Bundle.

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

## Installation from GitHub

The commands below apply after the proposed `v0.4.0` source tag is published.
This installs the published source tags into a clean SpecKit 0.16.2 project
without archives, GitHub Releases, or catalogs. It uses native local/dev
component installation and then registers the local Bundle against the four
already-installed component IDs.

```bash
specify --version # expected: specify 0.16.2

mkdir -p ~/src/speckit-governance
cd ~/src/speckit-governance
git clone --branch v1.0.1 --depth 1 https://github.com/ahhakopian/speckit-feature-governance.git
git clone --branch v0.4.0 --depth 1 https://github.com/ahhakopian/speckit-greenfield-governance.git

mkdir -p ~/projects/greenfield-project
cd ~/projects/greenfield-project
specify init --here --integration codex --ignore-agent-tools

specify extension add --dev ~/src/speckit-governance/speckit-feature-governance/extension --priority 10
specify preset add --dev ~/src/speckit-governance/speckit-feature-governance/preset --priority 10
specify workflow add --dev ~/src/speckit-governance/speckit-greenfield-governance/workflow
specify preset add --dev ~/src/speckit-governance/speckit-greenfield-governance/preset --priority 20

specify bundle install ~/src/speckit-governance/speckit-greenfield-governance --offline

specify preset list
specify extension list
specify workflow list
specify bundle list
```

`specify bundle install` records `speckit-greenfield-governance@0.4.0`; because
the four components are installed first, it resolves them locally and adds no
catalog dependency.

## Component resolution and publication

SpecKit 0.16.2 resolves Bundle component IDs through native primitive catalogs
or already-installed components; `bundle.yml` deliberately does not contain
relative paths or a custom installer. Publishing requires immutable GitHub
release artifacts and matching native catalog entries for the Workflow,
Greenfield Preset, Feature Governance Preset, and Feature Governance Extension,
then a Bundle release artifact and bundle-catalog entry.
