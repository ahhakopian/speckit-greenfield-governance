---
description: "Greenfield-owned ROADMAP completion after native convergence"
---

# Greenfield ROADMAP completion

Run only as the mandatory `after_converge` hook for the current Feature. This
command owns the ROADMAP status transition; it does not edit Feature artifacts,
product scope, the approved architecture, ordering, or dependencies.

1. Identify exactly one current Feature specification and its `ROADMAP entry: ID`
   line. If identity is missing or ambiguous, stop without changing ROADMAP.
2. Read the native converge outcome emitted immediately before this hook. Only
   `converged` (zero appended tasks) is clean. Independently check current
   implementation against the Canonical PRD, approved Architecture Baseline,
   and originating ROADMAP scope, responsibility, and dependencies. Apply the
   Greenfield final compatibility and conditional UX/UI rules, including
   required rendered evidence and specialist reviews for material UI. Require
   `COMPATIBLE`. The converge addendum's reported classification is supporting
   context, not a substitute for this current check. If either result is
   missing or uncertain, report that exact blocker and leave status `active`.
3. Rerun the **installed** Feature Governance review against the current
   Feature twice, once for the post-tasks checkpoint and once for the
   pre-implement checkpoint. Require the exact leading line
   `FEATURE_GOVERNANCE: PASS` on both fresh results. Rerun the installed MVP
   complexity preflight and post-implementation simplification review against
   the current artifacts; require each to report
   `MVP_COMPLEXITY_GUARD: PASS`. Missing commands, unavailable capabilities,
   `BLOCK`, `EXCEPTION_REQUIRED`, or ambiguous output block completion. Do not
   substitute a Greenfield review for any installed guard.
4. Inspect the current `tasks.md`, applicable acceptance checks, actual
   implementation, and required test/runtime evidence. Run the verification
   required by the Feature and relevant governance. Identify at least one
   existing project-relative evidence file. For material UI, include the
   current rendered evidence required by Greenfield convergence. Confirm that
   there is no unresolved product, architecture, Feature Governance, MVP, or
   Greenfield finding. A fixable missing check leaves the Feature active;
   request human input only for a genuinely new governed decision.
5. Invoke `python3 .specify/extensions/greenfield-roadmap-lifecycle/scripts/roadmap_lifecycle.py
   complete <ID>` with `--converge clean`, `--compatibility COMPATIBLE`,
   `--feature-after-tasks PASS`, `--feature-before-implement PASS`,
   `--mvp-before-implement PASS`, `--mvp-after-implement PASS`,
   `--verification PASS`, `--blockers none`, and one or more
   `--evidence <project-relative-path>` arguments **only after** all preceding
   checks actually passed. Use ordinary shell quoting for paths. The script
   independently checks ROADMAP identity, dependencies, tasks, and evidence
   file existence. Report its JSON result, including each affected dependent.

If any check fails, do not supply a PASS flag. Leave ROADMAP unchanged and
report the exact blocker. A rerun after remediation repeats the current checks.
