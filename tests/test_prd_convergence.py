"""SpecKit 0.16.2 PRD convergence lifecycle tests.

Run with the Python interpreter from the installed specify-cli environment.
The real engine owns persistence, nested replay, and gate behavior; only model
responses are stubbed. These tests do not assert arbitrary model correctness.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from specify_cli.workflows.base import RunStatus, StepResult, StepStatus
from specify_cli.workflows.engine import (
    WorkflowDefinition,
    WorkflowEngine,
    validate_workflow,
)
from specify_cli.workflows.expressions import evaluate_expression
from specify_cli.workflows.steps.prompt import PromptStep


WORKFLOW = Path(__file__).resolve().parents[1] / "workflow" / "workflow.yml"


class PrdConvergenceTests(TestCase):
    def setUp(self) -> None:
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name)
        self.prd = self.project / "prd.md"
        self.engine = WorkflowEngine(self.project)
        self.events: list[tuple[str, str, str, str]] = []
        self.rendered_apply_prompts: list[str] = []

        source = WorkflowDefinition.from_yaml(WORKFLOW)
        self.assertEqual(validate_workflow(source), [])
        data = deepcopy(source.data)
        # Stop at the existing architecture boundary so later foundation gates
        # do not obscure this focused PRD lifecycle test.
        data["steps"] = data["steps"][:2]
        self.workflow = WorkflowDefinition(data, source_path=WORKFLOW)

        def fake_prompt(_step: PromptStep, config: dict, context: object) -> StepResult:
            step_id = config["id"]
            decision = context.inputs["prd_decision"]
            comment = context.inputs["prd_comment"]
            before = self.prd.read_text(encoding="utf-8")
            self.events.append((step_id, decision, comment, before))

            if step_id == "apply-prd-resolution":
                self.rendered_apply_prompts.append(
                    evaluate_expression(config["prompt"], context)
                )
                if decision:
                    issue, separator, answer = decision.partition(":")
                    if separator and issue in {"gap-one", "gap-two"} and answer.strip():
                        marker = f"Decision {issue}: {answer.strip()}"
                        if marker not in before:
                            self.prd.write_text(before + marker + "\n", encoding="utf-8")
                return StepResult(status=StepStatus.COMPLETED)

            if step_id == "govern-prd":
                current = self.prd.read_text(encoding="utf-8")
                if "GAP_ONE" in current and "Decision gap-one:" not in current:
                    verdict = "PRODUCT GAP: gap-one"
                elif "GAP_TWO" in current and "Decision gap-two:" not in current:
                    verdict = "PRODUCT GAP: gap-two"
                else:
                    verdict = "CLEAN: no material PRODUCT GAP remains"
                # Real prompt stdout is streamed, not available to the gate.
                self.events.append(("review-verdict", verdict, "", current))
                return StepResult(
                    status=StepStatus.COMPLETED, output={"stdout": ""}
                )

            if step_id == "derive-review-architecture":
                return StepResult(status=StepStatus.COMPLETED)

            self.fail(f"Unexpected prompt step: {step_id}")

        prompt_patch = patch.object(PromptStep, "execute", fake_prompt)
        prompt_patch.start()
        self.addCleanup(prompt_patch.stop)

    def start(self, content: str):
        self.prd.write_text(content, encoding="utf-8")
        return self.engine.execute(
            self.workflow, {"canonical_prd": "prd.md", "integration": "auto"}
        )

    def resume(self, run_id: str, **inputs: str):
        return self.engine.resume(run_id, inputs)

    def reviews(self) -> list[str]:
        return [event[1] for event in self.events if event[0] == "review-verdict"]

    def architecture_reached(self) -> bool:
        return any(event[0] == "derive-review-architecture" for event in self.events)

    def test_clean_prd_requires_approval_before_architecture(self) -> None:
        state = self.start("Purpose and outcomes are defined.\n")
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertEqual(self.reviews(), ["CLEAN: no material PRODUCT GAP remains"])
        self.assertFalse(self.architecture_reached())

        state = self.resume(state.run_id, prd_gate_decision="approve")
        self.assertEqual(state.status, RunStatus.COMPLETED)
        self.assertEqual(len(self.reviews()), 2)
        self.assertTrue(self.architecture_reached())

    def test_one_gap_edit_full_review_and_approval(self) -> None:
        state = self.start("Purpose defined. GAP_ONE remains.\n")
        self.assertEqual(self.reviews(), ["PRODUCT GAP: gap-one"])
        state = self.resume(state.run_id, prd_gate_decision="reject")
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertEqual(state.inputs["prd_gate_decision"], "")
        self.assertFalse(self.architecture_reached())

        state = self.resume(state.run_id, prd_decision="gap-one: use consent")
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertIn("Decision gap-one: use consent", self.prd.read_text())
        self.assertEqual(self.reviews()[-1], "CLEAN: no material PRODUCT GAP remains")
        self.assertFalse(self.architecture_reached())

        state = self.resume(
            state.run_id,
            prd_gate_decision="approve",
            prd_decision="",
            prd_comment="",
        )
        self.assertEqual(state.status, RunStatus.COMPLETED)
        self.assertEqual(self.reviews()[-1], "CLEAN: no material PRODUCT GAP remains")
        self.assertTrue(self.architecture_reached())

    def test_two_gaps_repeat_in_same_run_without_stale_edit(self) -> None:
        state = self.start("Purpose defined. GAP_ONE and GAP_TWO remain.\n")
        run_id = state.run_id
        state = self.resume(run_id, prd_gate_decision="reject")
        self.assertEqual(state.status, RunStatus.PAUSED)
        state = self.resume(run_id, prd_decision="gap-one: use consent")
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertEqual(self.reviews()[-1], "PRODUCT GAP: gap-two")
        first_revision = self.prd.read_text()
        self.assertFalse(self.architecture_reached())

        # The previous answer persists through replay. It must not be applied
        # a second time or used to answer the next question.
        state = self.resume(run_id, prd_gate_decision="reject")
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertEqual(self.prd.read_text(), first_revision)
        self.assertEqual(self.reviews()[-1], "PRODUCT GAP: gap-two")
        self.assertEqual(state.inputs["prd_gate_decision"], "")

        state = self.resume(
            run_id,
            prd_decision="gap-two: retain for thirty days",
            prd_comment="chosen by product owner",
        )
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertEqual(self.reviews()[-1], "CLEAN: no material PRODUCT GAP remains")
        self.assertFalse(self.architecture_reached())
        self.assertIn("gap-two: retain for thirty days", self.rendered_apply_prompts[-1])
        self.assertIn("chosen by product owner", self.rendered_apply_prompts[-1])
        self.assertNotIn("chosen by product owner", self.prd.read_text())

        state = self.resume(
            run_id,
            prd_gate_decision="approve",
            prd_decision="",
            prd_comment="",
        )
        self.assertEqual(state.status, RunStatus.COMPLETED)
        self.assertEqual(state.run_id, run_id)
        self.assertTrue(self.architecture_reached())
        self.assertEqual(state.inputs["prd_decision"], "")
        self.assertEqual(state.inputs["prd_comment"], "")
        self.assertEqual(self.prd.read_text().count("Decision gap-one:"), 1)
        self.assertEqual(self.prd.read_text().count("Decision gap-two:"), 1)

    def test_replayed_decision_is_idempotent_and_comment_alone_is_no_op(self) -> None:
        state = self.start("GAP_ONE remains.\n")
        state = self.resume(state.run_id, prd_gate_decision="reject")
        state = self.resume(
            state.run_id,
            prd_decision="gap-one: custom product behavior",
            prd_comment="background only",
        )
        edited = self.prd.read_text()
        self.assertNotIn("background only", edited)

        state = self.resume(state.run_id)
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertEqual(self.prd.read_text(), edited)
        self.assertEqual(self.prd.read_text().count("Decision gap-one:"), 1)

        state = self.resume(
            state.run_id, prd_decision="", prd_comment="comment by itself"
        )
        self.assertEqual(state.status, RunStatus.PAUSED)
        self.assertEqual(self.prd.read_text(), edited)
        self.assertEqual(state.inputs["prd_decision"], "")

    def test_downstream_deferral_and_resolved_requirement_are_clean(self) -> None:
        for text in (
            "Product behavior defined; architecture topology is deferred.\n",
            "An earlier section resolves the requirement.\n",
        ):
            with self.subTest(prd=text):
                self.events.clear()
                state = self.start(text)
                self.assertEqual(state.status, RunStatus.PAUSED)
                self.assertEqual(
                    self.reviews()[-1], "CLEAN: no material PRODUCT GAP remains"
                )
                state = self.resume(state.run_id, prd_gate_decision="approve")
                self.assertEqual(state.status, RunStatus.COMPLETED)
                self.assertTrue(self.architecture_reached())

    def test_loop_cap_cannot_advance_rejected_gate(self) -> None:
        convergence = self.workflow.steps[0]
        self.assertEqual(convergence["type"], "do-while")
        self.assertIs(convergence["condition"], False)
        self.assertEqual(convergence["max_iterations"], 1)
        self.assertEqual(convergence["steps"][-1]["on_reject"], "retry")

        state = self.start("GAP_ONE remains.\n")
        for _ in range(2):
            state = self.resume(state.run_id, prd_gate_decision="reject")
            self.assertEqual(state.status, RunStatus.PAUSED)
            self.assertFalse(self.architecture_reached())
            self.assertEqual(self.reviews()[-1], "PRODUCT GAP: gap-one")

    def test_prompt_contracts_are_explicit(self) -> None:
        apply_step, review_step, gate = self.workflow.steps[0]["steps"]
        apply_prompt = apply_step["prompt"]
        review_prompt = review_step["prompt"]
        self.assertIn("If the decision is blank, make no change", apply_prompt)
        self.assertIn("comment alone creates no", apply_prompt)
        self.assertIn("already fully represented", apply_prompt)
        self.assertIn("Do not expand product scope", apply_prompt)
        self.assertIn("make no edit and clearly report why", apply_prompt)
        self.assertIn("ENTIRE current Canonical", review_prompt)
        self.assertIn("reconcile each candidate issue", review_prompt)
        self.assertIn("requirements elsewhere", review_prompt)
        self.assertIn("explicit downstream deferrals", review_prompt)
        self.assertIn("immaterial underspecification", review_prompt)
        self.assertIn("already resolved behavior", review_prompt)
        self.assertIn("exactly ONE actionable product question", review_prompt)
        self.assertIn("no material PRODUCT GAP remains", review_prompt)
        self.assertIn("immediately preceding govern-prd response", gate["message"])
        self.assertIn("prd_decision=", gate["message"])
        self.assertIn("prd_comment=", gate["message"])
