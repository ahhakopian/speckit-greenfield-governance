# Greenfield Governance Policy

## 1. Purpose and Scope

This document is the sole semantic implementation contract for the
`speckit-greenfield-governance` add-on. Subsequent design and implementation
phases MUST preserve the authorities, classifications, escalation paths, and
scope boundaries defined here.

The policy governs two processes:

1. greenfield foundation, from an untrusted Canonical PRD to `PROJECT READY`;
2. integration of ordinary SpecKit Feature work with the approved project
   architecture and cross-Feature roadmap.

The required foundation lifecycle is:

```text
Untrusted Canonical PRD
-> PRD Governance Gate
-> derive TARGET Architecture
-> Architecture Review
-> Approved architecture/baseline.md
-> derive ROADMAP.md
-> derive/update Constitution through native SpecKit
-> PROJECT READY
```

The Feature lifecycle begins only after `PROJECT READY` and is defined once in
Section 9.

The policy defines semantics, not packaging. It MUST NOT prescribe manifest
schemas, installation machinery, agent-specific invocation syntax, or changes
to SpecKit Core.

The accepted minimum composition is one foundation-only `greenfield-bootstrap`
Workflow, one thin Preset for `specify`, `clarify`, `plan`, and `converge`, an
extension of the existing `speckit-feature-governance` checks, and one Bundle
used only for distribution and composition. This composition is a constraint,
not authorization to implement those components in the current phase.

## 2. Source Authority and Sources of Truth

Authority is determined by subject. No artifact MAY silently assume authority
over a subject assigned to another artifact.

| Artifact | Exclusive or primary authority |
|---|---|
| Canonical PRD | Product and system intent; scope; actors; capabilities; authority; ownership; and product boundaries |
| `architecture/baseline.md` | Approved TARGET Architecture |
| `ROADMAP.md` | Feature decomposition; Feature boundaries; cross-Feature dependencies and order; architecture responsibility; and Feature status |
| Constitution | Cross-cutting invariants that apply across Features and implementation work |
| `specs/**` | Feature-local requirements, clarification, design, planning, and tasks |

These authorities are complementary:

- the Canonical PRD defines what the product or system is and who owns product
  decisions;
- the Architecture Baseline defines the approved technical realization and
  durable architecture constraints;
- the ROADMAP divides approved product and architecture scope into ordered,
  bounded Features;
- the Constitution governs cross-cutting principles without restating product
  or architecture content;
- Feature artifacts elaborate one ROADMAP entry without changing upstream
  authorities.

Current code, historical documents, generated plans, completed tasks, and model
output are evidence only. None of them overrides an authoritative source merely
because it exists or appears more detailed.

When authoritative artifacts conflict, work MUST stop at the earliest phase
affected. The conflict MUST be resolved in the artifact that owns the disputed
subject before downstream work continues.

For UX/UI governance, authority is likewise determined by subject:

- product artifacts own product meaning and scope;
- `spec.md` owns user-observable Feature behavior;
- `DESIGN.md`, when present, owns reusable cross-Feature or surface UX/UI
  rules;
- an optional surface artifact owns only durable, surface-specific presentation
  decisions that have no better authority; and
- `plan.md` owns technical realization.

UX/UI craft, evidence, or a tool result MUST NOT silently change an authority
owned by any of these artifacts.

## 3. PRD Governance Gate

The Canonical PRD MUST initially be treated as untrusted input even though it is
the designated product/system source of truth. “Canonical” identifies where
product decisions belong; it does not prove that the current content is
complete, consistent, approved, safe to interpret, or sufficient for TARGET
Architecture derivation.

The PRD Governance Gate MUST evaluate at least:

- declared product/system purpose and scope;
- actors and materially distinct responsibilities;
- required capabilities and observable outcomes;
- authority and ownership of important decisions, policy, and state;
- product boundaries, explicit exclusions, and deferred scope;
- trust, access, consent, privacy, lifecycle, and external-system expectations
  where material to the product;
- contradictions, unresolved high-impact ambiguity, and unsupported implied
  scope;
- whether the information needed to begin architecture derivation is present.

The gate MUST NOT select APIs, services, frameworks, databases, deployment
topology, or other architecture choices. Missing technical realization is not,
by itself, a PRD defect.

The gate passes only when no blocking `PRODUCT GAP` remains. The governed PRD
revision then becomes trusted as input to architecture derivation; this trust is
limited to its product authority and does not approve any architecture.

The gate MUST expose its gap classifications for explicit human acceptance.
Human acceptance MAY allow declared `ARCHITECTURE GAP` items to proceed, but it
MUST NOT waive a `PRODUCT GAP`; the Canonical PRD must first be corrected.

Gate findings MUST be reported in the active interaction. Native workflow state
MAY record the gate outcome. The overlay MUST NOT create a separate PRD-review
artifact.

## 4. Product Gap vs Architecture Gap

Every material issue found while governing the PRD MUST be classified by the
authority required to resolve it.

### PRODUCT GAP

A `PRODUCT GAP` exists when a missing, contradictory, or unresolved decision
changes or could materially change any of the following:

- product/system intent or scope;
- actors, roles, or capabilities;
- product responsibility or product boundary;
- authority or ownership;
- access, consent, or policy semantics;
- required outcome, lifecycle behavior, or explicit exclusion;
- whether a capability belongs to the current product or milestone.

A `PRODUCT GAP` is blocking. Architecture derivation MUST stop. The Canonical
PRD MUST be changed through its normal human-controlled process, and the PRD
Governance Gate MUST be run again. Architecture, ROADMAP, Constitution, and
Feature artifacts MUST NOT resolve or conceal the gap.

### ARCHITECTURE GAP

An `ARCHITECTURE GAP` exists when approved product intent is sufficiently clear
but its technical realization is unspecified. Examples include component
responsibility, runtime boundaries, contracts, validation placement, state
ownership, persistence, lifecycle realization, compatibility, or deployment
constraints.

An `ARCHITECTURE GAP` is permitted to proceed to architecture derivation. Its
resolution MUST preserve the Canonical PRD and follow the architecture approval
rules in this policy.

If an issue contains both product and architecture uncertainty, it MUST be
treated as a `PRODUCT GAP` until the product part is resolved.

## 5. Architecture Derivation and Approval

TARGET Architecture MUST be derived from the governed Canonical PRD. It MAY
choose technical structure where the PRD intentionally leaves that structure
open, but it MUST NOT silently narrow, broaden, reinterpret, or contradict
product scope, authority, ownership, capabilities, or boundaries.

Architecture derivation MUST distinguish evidence from inference and MUST make
material uncertainty explicit. Conventional layers, services, actors, stores,
or deployment units MUST NOT be invented without a product requirement,
technical constraint, or demonstrated architectural need.

Architecture Review MUST determine whether the proposed TARGET Architecture:

- covers the governed PRD without changing it;
- assigns coherent component and contract responsibilities;
- identifies authority, ownership, trust transitions, validation, and important
  state/lifecycle behavior;
- makes dependencies and cross-Feature architecture responsibilities usable for
  ROADMAP derivation;
- is internally consistent and implementable;
- leaves no unresolved material decision that would produce materially
  different durable architectures.

A material architecture decision MUST NOT be selected silently. A decision is
material when it has durable or cross-Feature consequences, including a change
to a public or external contract, authority or ownership, a trust boundary,
persistent-state lifecycle or compatibility, runtime/deployment boundary, or
cross-Feature architecture responsibility.

Material alternatives and consequences MUST be presented for human decision.
An ADR MAY be created only when the decision is both material and sufficiently
long-lived that preserving rationale outside the baseline is justified. ADRs
MUST NOT be mandatory, automatic, or created for ordinary reversible design
choices. Approval and the operative decision MUST remain visible in the
Architecture Baseline even when an ADR exists.

Only explicit human approval changes the baseline from draft to approved.
Silence, generated text, implementation, tests, or workflow completion MUST NOT
be interpreted as approval.

## 6. Architecture Baseline Contract

`architecture/baseline.md` is the single Approved TARGET Architecture source of
truth. Before approval it is a draft candidate and MUST NOT govern Feature
implementation as an approved baseline.

The baseline MUST contain enough information to evaluate Feature compatibility,
including, where relevant:

- approval status and revision identity;
- system context, scope assumptions, and technical boundaries;
- architectural components and their responsibilities;
- authoritative owners of important decisions and state;
- communication, integration, and trust boundaries;
- validation and authorization placement;
- important contracts and dependency directions;
- persistent state, lifecycle, migration, and compatibility rules;
- runtime and deployment constraints;
- cross-cutting quality or operational constraints that are architectural;
- explicit architecture responsibility available for ROADMAP assignment;
- unresolved non-blocking gaps and the conditions under which they become
  blocking.

The baseline MUST NOT duplicate the Canonical PRD, decompose work into Features,
or become an implementation task list. It MAY refer to product requirements and
ROADMAP entries, but no separate traceability artifact is required.

An approved baseline is stable by default. It MUST NOT be edited as an incidental
result of `specify`, `clarify`, `plan`, `tasks`, implementation, convergence, or
release. Material changes require the Controlled Architecture Change lifecycle.

## 7. ROADMAP Contract

`ROADMAP.md` is the project-level Spec-of-Specs for Feature decomposition and
sequencing. It is not product authority, architecture authority, a Feature
specification, an implementation plan, or authorization to implement.

Each actionable ROADMAP entry MUST define at least:

- a stable local entry identifier;
- intended outcome;
- scope boundary and relevant non-goals;
- architecture responsibility assigned to the Feature;
- dependencies and ordering constraints;
- status;
- a link to the corresponding Feature specification when one exists.

The minimum status vocabulary is `planned`, `ready`, `active`, `blocked`,
`deferred`, and `done`. `ready` means that declared dependencies and required
upstream decisions permit specification to start; `done` has the release
meaning defined below.

Feature specifications MUST identify their originating ROADMAP entry. Plain
text links in both directions are sufficient; a separate traceability system
MUST NOT be introduced.

ROADMAP order MUST follow meaningful product, authority, contract, lifecycle,
architecture-responsibility, and verification dependencies. Shared file impact
alone is not a dependency.

The ROADMAP MAY change directly when only Feature decomposition, boundaries,
ordering, or status changes and the Canonical PRD and Architecture Baseline
remain valid. The ROADMAP MUST NOT approve new product scope or a new material
architecture decision.

An entry may be released only when its dependencies are satisfied and the final
compatibility rule passes. Its status becomes `done` only after successful
release, not merely after tasks or implementation complete.

## 8. Constitution Relationship

The Constitution MUST be derived or updated through native SpecKit only after
the Architecture Baseline is approved and the initial ROADMAP exists.

The Constitution contains only durable cross-cutting invariants, such as quality,
safety, testing, privacy, or engineering rules that genuinely govern multiple
Features. It MUST NOT copy or replace:

- product scope, actors, capabilities, authority, ownership, or product
  boundaries from the Canonical PRD;
- components, contracts, state ownership, trust boundaries, or topology from
  the Architecture Baseline;
- Feature decomposition, dependencies, order, responsibility, or status from
  the ROADMAP.

If a proposed constitutional rule changes product meaning, it MUST be resolved
in the Canonical PRD. If it changes TARGET Architecture, it MUST use Controlled
Architecture Change. If it changes only Feature decomposition or order, it
belongs in the ROADMAP.

`PROJECT READY` requires all of the following:

1. the PRD Governance Gate has no blocking `PRODUCT GAP`;
2. `architecture/baseline.md` is explicitly approved;
3. `ROADMAP.md` defines an actionable, dependency-aware decomposition;
4. the Constitution has been derived or reconciled through native SpecKit;
5. no unresolved conflict exists among these authorities.

## 9. Feature Lifecycle Integration

Only a ready, unblocked ROADMAP entry may enter the ordinary SpecKit Feature
lifecycle. The `greenfield-bootstrap` Workflow ends at `PROJECT READY` and MUST
NOT orchestrate Feature work.

The governed Feature lifecycle is:

```text
ROADMAP entry
-> specify
-> clarify
-> plan
-> tasks
-> existing Feature Governance Guard
-> analyze
-> existing pre-implement guard
-> implement
-> converge with final architecture compatibility check
-> release
-> ROADMAP status = done
```

Feature artifacts MAY elaborate requirements and make reversible implementation
choices within the authority granted by their ROADMAP entry and the approved
baseline. They MUST NOT silently change upstream product, architecture, or
cross-Feature decisions.

`tasks` MUST be derived from an already governed Feature specification and plan.
A task MUST NOT introduce a new product decision, material architecture decision,
Feature boundary, cross-Feature dependency, or architecture responsibility. If
task generation discovers such a decision, task generation MUST stop and route
the issue to the owning authority.

Native `analyze` remains the read-only Feature artifact consistency phase. It
does not become a second baseline or roadmap governance mechanism.

## 10. Escalation Rules for `specify`, `clarify`, and `plan`

At every phase, first classify the discovered issue by the authority that must
change.

### `specify`

`specify` MUST keep the Feature within its ROADMAP outcome, scope boundary,
architecture responsibility, and approved baseline.

- A new or changed product scope, capability, actor, authority, ownership, or
  product boundary is a product-level escalation: stop and return to the
  Canonical PRD.
- A material change to approved architecture is an architecture-level
  escalation: classify `BASELINE_CHANGE_REQUIRED` and stop.
- A change only to Feature decomposition, boundary, dependency, or order is a
  ROADMAP escalation.
- Feature-local detail consistent with all three authorities may remain in
  `spec.md`.

### `clarify`

`clarify` MAY resolve Feature-local ambiguity, but the answer's authority is
determined by its effect, not by where the question was asked.

- Product-significant answers MUST be approved in the Canonical PRD before they
  are used by the Feature.
- Material architecture answers MUST follow Controlled Architecture Change.
- Decomposition or ordering answers MUST update the ROADMAP.
- Only Feature-local answers MAY be written directly to Feature artifacts
  without upstream escalation.

Clarification MUST NOT use a leading or implementation-convenient question to
manufacture permission for an upstream change.

### `plan`

`plan` MAY select reversible implementation details inside the approved
Architecture Baseline. It MUST evaluate the proposed design against the baseline
and ROADMAP architecture responsibility before tasks are produced.

If the plan needs a material architecture decision not already permitted by the
baseline, it MUST present realistic alternatives and consequences for human
decision. When the chosen decision changes the baseline, the result is
`BASELINE_CHANGE_REQUIRED`; planning stops until Controlled Architecture Change
completes. Tasks MUST NOT be generated from a plan with unresolved product or
architecture escalation.

## 11. Architecture Compatibility Classification

Every governed Feature design and final implementation MUST receive exactly one
of these classifications:

### COMPATIBLE

Use `COMPATIBLE` only when the Feature:

- preserves the Canonical PRD;
- conforms to the current approved Architecture Baseline;
- stays within its ROADMAP boundary and architecture responsibility;
- respects declared dependencies and dependency direction;
- introduces no unapproved material architecture decision.

Differences in reversible implementation detail are compatible when the
baseline intentionally leaves them open.

### BASELINE_CHANGE_REQUIRED

Use `BASELINE_CHANGE_REQUIRED` when correct delivery requires adding, removing,
or materially changing approved architecture, including a component
responsibility, authority or state ownership, trust or runtime boundary,
important contract, persistence/lifecycle/compatibility rule, dependency
direction, or cross-Feature architecture responsibility.

This classification is not approval and MUST block downstream implementation or
release until Controlled Architecture Change completes.

If the underlying conflict actually changes product scope, authority, ownership,
or a product boundary, it is not resolved as architecture change; it is a
product-level escalation to the Canonical PRD.

A ROADMAP-only decomposition or ordering change is not, by itself,
`BASELINE_CHANGE_REQUIRED`.

## 12. Controlled Architecture Change Lifecycle

Approved architecture MAY evolve, but only deliberately. A Controlled
Architecture Change MUST use this lifecycle:

1. classify the Feature or implementation as `BASELINE_CHANGE_REQUIRED` and
   stop the affected downstream phase;
2. identify the exact approved baseline statements affected, the binding need,
   realistic compatible alternatives considered, and the material consequences;
3. identify affected ROADMAP entries and dependencies without expanding the
   review to unrelated entries;
4. obtain an explicit human decision;
5. if rejected, preserve the approved baseline and revise, defer, or stop the
   Feature;
6. if approved, update the relevant baseline content and approval/revision state;
7. update ROADMAP architecture responsibility or dependencies only where the
   approved baseline change requires it;
8. revalidate only affected downstream ROADMAP entries and restart each affected
   Feature from its earliest invalidated phase;
9. do not resume implementation or release until the current Feature is again
   classified `COMPATIBLE`.

The lifecycle MUST NOT require a separate architecture-change or review artifact.
The active Feature plan may describe the conflict and alternatives, but it does
not become architecture authority. The approved decision is incorporated into
the baseline; resulting decomposition changes are incorporated into the ROADMAP.

If baseline content and ROADMAP dependencies remain unchanged, completing a
Feature MUST NOT trigger full project-wide reanalysis. Revalidation is scoped to
the current Feature and any downstream entries directly affected by an approved
change.

## 13. Existing Feature Governance Guard Integration

The existing `speckit-feature-governance` policy remains authoritative for
Feature boundary cohesion, forward evolution, dependency direction, downstream
ignorance, and its established exception handling. This overlay MUST reuse and
extend it rather than reproduce those rules.

A Feature Governance exception or approval does not authorize a product or
Architecture Baseline change. If the same proposal affects product authority or
approved architecture, the Canonical PRD or Controlled Architecture Change
process respectively MUST complete in addition to the existing Feature
Governance process.

Its existing post-`tasks` and pre-`implement` guard checkpoints MUST additionally
verify:

- the Feature is linked to an actionable ROADMAP entry;
- `spec.md`, `plan.md`, and `tasks.md` stay within the entry's scope and
  architecture responsibility;
- the Feature is `COMPATIBLE` with the approved Architecture Baseline;
- ROADMAP dependencies and ordering are satisfied;
- tasks contain no new product or material architecture decision;
- any proposed change is routed to the correct authority before implementation.

The pre-implement checkpoint MUST repeat the compatibility decision after
`analyze` or intervening edits. A non-compatible result blocks implementation.

No second governance guard and no additional `after_tasks` or
`before_implement` hook may be introduced for these checks.

## 14. Final Architecture Compatibility and Release

`converge` MUST assess the implementation against all three applicable levels:

1. Feature-local artifacts;
2. the approved Architecture Baseline;
3. the ROADMAP entry's architecture responsibility and dependencies.

The final architecture compatibility check is part of governed convergence; it
MUST NOT require an `after_converge` hook or a separate review artifact.

Release is permitted only when:

- required Feature work is complete;
- Feature artifacts and implementation agree;
- final classification is `COMPATIBLE`;
- the implementation satisfies the approved baseline;
- the ROADMAP architecture responsibility is fulfilled;
- required upstream ROADMAP dependencies are done or otherwise satisfied under
  the roadmap's explicit rules;
- no unresolved product, architecture, or governance blocker remains.

`BASELINE_CHANGE_REQUIRED` blocks release. The change MUST complete its
controlled lifecycle and the Feature MUST reconverge before release is
reconsidered.

The ROADMAP entry status becomes `done` only after successful release. The
overlay does not define or replace the project's release tooling.

## 15. Conditional UX/UI Governance

UX/UI governance applies only when a Feature materially changes a user-facing
surface or interaction. Merely touching frontend code is not sufficient. It
does not change the ownership of SpecKit, the existing Feature Governance, or
the existing MVP Governance: SpecKit remains lifecycle owner; Feature
Governance remains authoritative for Feature boundaries and evolution; and MVP
Governance remains authoritative for simplicity and complexity control.

### Pre-plan UX/UI decision

Before technical planning, ask: **Does this Feature require a new UX
decision?** First determine whether the Feature materially changes a
user-facing surface or interaction.

- If it does not, continue ordinary SpecKit planning.
- If an established UX/UI pattern fully determines the change, identify and
  reuse that pattern, then continue without shaping.
- Otherwise, invoke the installed Impeccable shape capability, bounded to the
  current Feature and affected surfaces.
- If that capability is unavailable or cannot run, stop the affected planning
  phase and report the missing capability. Do not perform custom availability
  detection or substitute generic UX reasoning.

Availability is implicit in the named capability invocation; this overlay MUST
NOT add availability detection.

Classify the shaping outcome by authority. A shaping outcome that changes
product meaning or scope MUST be routed to its owning product authority. If it
introduces or changes user-observable Feature behavior, technical planning MUST
stop until `spec.md` is reconciled and revalidated. Purely presentational
decisions MUST NOT be copied into `spec.md`. Impeccable craft or shaping MUST
NOT replace SpecKit planning, task generation, or implementation.

### UX/UI artifact YAGNI

Shaping MAY complete without creating an artifact. `DESIGN.md` is not required
merely because UI exists; create or update it only when a concrete reusable
UX/UI rule emerges. A `.impeccable/surfaces/*` artifact is not required for
every UI Feature and is permitted only for a durable, surface-local
presentation decision that must survive and has no better authority. A UX
review report is not required. Native Impeccable review snapshots are
tool-owned evidence, not governance authority.

### Post-implementation UX/UI convergence

During convergence, determine from both Feature intent and the actual
implementation whether user-facing UI was materially changed. For material UI,
current rendered evidence in the target runtime is required for the affected
flow or states and representative viewport or device classes as appropriate.
For browser-based surfaces, rendered browser evidence satisfies this
requirement. Evaluate only against applicable authority: reconciled `spec.md`,
relevant upstream product constraints, applicable `DESIGN.md`, and applicable
surface-specific decisions. This focused check MUST NOT become a full product
re-audit.

Select specialist review in proportion to actual risk:

- When UX or interaction quality is materially at risk, invoke the installed
  Impeccable critique capability for the affected Feature and surfaces.
- When accessibility, responsiveness, theming, performance, or implementation
  integrity is materially at risk, invoke the installed Impeccable audit
  capability for the affected Feature and surfaces.
- Invoke both only when the change spans both categories or is a substantial
  new or redesigned surface.

If a required named capability is unavailable or cannot run, stop the affected
convergence phase and report the missing capability; do not substitute generic
UX reasoning or add custom availability detection. Material findings MUST be
resolved before convergence. After a material fix, reverify the affected
behavior. Polish is optional and finding-driven. UX/UI conditions MUST pass
before the existing final `COMPATIBLE` classification is returned.

UX/UI governance introduces no extension, lifecycle hook, workflow, SpecKit
command, governance aggregator, or mandatory artifact type.

## 16. Project-Owned and Overlay-Owned Artifacts

The following are project-owned and MUST survive add-on removal:

- the Canonical PRD;
- `architecture/baseline.md`;
- `ROADMAP.md`;
- `.specify/memory/constitution.md`;
- `specs/**` and their normal Feature-local contents;
- `DESIGN.md`, when present;
- durable `.impeccable/surfaces/*` artifacts, when present; and
- any project-owned ADR that was independently justified under this policy.

Project-owned artifacts MUST NOT be treated as files owned by the add-on's
distribution lifecycle. Add-on removal MUST NOT delete, roll back, or replace
their approved content.

Native Impeccable critique or review snapshots remain tool-owned evidence and
MUST NOT be treated as project-owned governance authority.

Overlay-owned content is limited to the semantic policy and, in later authorized
phases, the approved minimum Workflow, Preset, existing Feature Governance
extension changes, and Bundle metadata needed to deliver this policy. Generated
project decisions and Feature artifacts are not overlay-owned merely because
overlay behavior helped create or update them.

## 17. Explicit Non-Goals and Prohibited Complexity

The externally installed Impeccable shape, critique, and audit capabilities are
runtime prerequisites when applicable. They are not overlay-owned components.

This overlay MUST NOT add or require:

- a full Feature lifecycle inside `greenfield-bootstrap`;
- `full`, `foundation`, or `feature` bootstrap modes;
- separate `prd-review`, `architecture-derive`, `architecture-review`,
  `architecture-approve`, `roadmap`, `feature-compatibility`, or
  `final-compatibility` commands;
- a second governance guard;
- new `after_tasks` or `before_implement` hooks in addition to the existing
  Feature Governance Guard hooks;
- an `after_converge` hook;
- Preset wrappers or addenda for `tasks`, `analyze`, or `constitution`;
- Product Model, Access Model, or Product Boundaries artifacts;
- a traceability artifact, database, or registry;
- a PRD-review or architecture-review report;
- a mandatory ADR system;
- an architecture-change artifact;
- a custom release artifact or release engine;
- a custom installer, global wrapper, source cache, synchronization mechanism,
  package lifecycle, or uninstall lifecycle;
- a native workflow overlay in place of the standalone foundation Workflow;
- new workflow step types, shell-based governance, or parallel orchestration;
- a new or custom overlay-owned UX/UI skill, extension, lifecycle hook,
  workflow, SpecKit command, governance aggregator, mandatory artifact type,
  wrapper, registry, or installer;
- modifications to SpecKit Core;
- automatic approval, automatic product-policy selection, or silent mutation of
  an authoritative source.

The overlay MUST use native SpecKit behavior where the approved composition
assigns it responsibility. It MUST remain no larger than required to carry this
policy into foundation and ordinary Feature work.
