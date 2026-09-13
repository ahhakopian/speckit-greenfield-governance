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

## Component resolution and publication

SpecKit 0.16.2 resolves Bundle component IDs through native primitive catalogs
or already-installed components; `bundle.yml` deliberately does not contain
relative paths or a custom installer. Publishing requires immutable GitHub
release artifacts and matching native catalog entries for the Workflow,
Greenfield Preset, Feature Governance Preset, and Feature Governance Extension,
then a Bundle release artifact and bundle-catalog entry.
