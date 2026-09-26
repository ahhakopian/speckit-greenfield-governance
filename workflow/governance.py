"""Fail-closed PRD review ledger for the SpecKit 0.16.2 workflow package.

The run-local ledger is audit/debug state, never product authority. The canonical
PRD remains the only product document. Shell steps capture JSON from this helper;
model stdout is never used as a verdict.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

RUN_ID = re.compile(r"[A-Za-z0-9_-]+\Z")
GAP_ID = re.compile(r"[a-z][a-z0-9-]*\Z")
INTERNAL_TEXT = re.compile(
    r"\b(?:run[ -]?id|git status|resume with|govern-prd|prd-governance|"
    r"workflow stage)\b|\.specify/|--input|\b[a-fA-F0-9]{64}\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise ValueError(message)


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"Expected JSON object: {path}")
    return data


def save_json(path: Path, data: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def revision(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def required_string(data: dict, key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"Review field {key!r} must be a nonempty string")
    return value.strip()


def gap_from_submission(item: object) -> dict:
    if not isinstance(item, dict):
        fail("Each PRODUCT GAP must be an object")
    gap_id = required_string(item, "gap_id")
    if not GAP_ID.fullmatch(gap_id):
        fail("PRODUCT GAP gap_id must be a stable lowercase slug")
    options = item.get("options")
    if not isinstance(options, list) or len(options) < 2 or any(
        not isinstance(option, str) or not option.strip() for option in options
    ):
        fail("PRODUCT GAP options must contain at least two nonempty choices")
    recommended = item.get("recommended_option")
    if not isinstance(recommended, int) or isinstance(recommended, bool) or not 1 <= recommended <= len(options):
        fail("recommended_option must be an option number")
    return {
        "gap_id": gap_id,
        "question": required_string(item, "question"),
        "options": [option.strip() for option in options],
        "recommended_option": recommended,
        "rationale": required_string(item, "rationale"),
    }


def question_key(question: str) -> str:
    """Collapse superficial wording differences for deterministic rediscovery."""
    return " ".join(re.findall(r"[\w]+", question.casefold()))


def validate_human_fields(gap: dict, run_id: str) -> None:
    for value in [gap["question"], *gap["options"], gap["rationale"]]:
        if re.search(rf"(?<![\w-]){re.escape(run_id)}(?![\w-])", value) or INTERNAL_TEXT.search(value):
            fail("PRODUCT GAP human text contains workflow diagnostics")


def gap_message(gap: dict) -> str:
    lines = ["Decision required", "", gap["question"], ""]
    lines.extend(f"{index}. {option}" for index, option in enumerate(gap["options"], 1))
    lines.extend([
        f"{len(gap['options']) + 1}. Custom rule (write it out).", "", "Recommended:",
        f"{gap['recommended_option']} — {gap['rationale']}", "",
        f"Please choose 1–{len(gap['options'])}, or provide a custom rule.",
    ])
    return "\n".join(lines)


def approval_message() -> str:
    return ("PRD review complete\n\nNo unresolved product gaps remain.\n\n"
            "Approve this PRD as the basis for architecture?\n\n"
            "Recommended:\nApprove.\n\nPlease reply: Approve or Reject.")


def main(stage: str, run_id: str) -> dict:
    if not RUN_ID.fullmatch(run_id):
        fail("Invalid run ID")
    root = Path.cwd().resolve()
    run_dir = root / ".specify" / "workflows" / "runs" / run_id
    inputs = read_json(run_dir / "inputs.json")["inputs"]
    prd = (root / inputs["canonical_prd"]).resolve()
    if not prd.is_relative_to(root) or not prd.is_file():
        fail("Canonical PRD must be an existing project file")
    ledger_path = run_dir / "prd-governance.json"
    receipt_path = run_dir / "prd-review-submission.json"
    ledger = read_json(ledger_path) if ledger_path.exists() else {
        "schema_version": 1, "reviews": [], "unresolved_gaps": [],
        "resolved_gaps": [], "approval": None, "pending_gap_id": None,
        "last_decision_key": None, "pending_resolution": None,
    }
    current = revision(prd)

    if stage == "prepare":
        previous = ledger["reviews"][-1] if ledger["reviews"] else None
        requested = inputs.get("prd_gate_decision") == "approve"
        ledger["approval_request_revision"] = (
            previous["prd_revision"] if requested and previous and
            previous["effective_verdict"] == "CLEAN" else None
        )
        decision = inputs.get("prd_decision", "").strip()
        gap_id = ledger.get("pending_gap_id")
        # Inputs persist across resumes. The same answer must
        # never be rebound to a different gap merely because the pending gap
        # changed after a prior review.
        decision_key = hashlib.sha256(decision.encode()).hexdigest() if gap_id and decision else None
        fresh = bool(decision_key and decision_key != ledger.get("last_decision_key"))
        if not decision:
            ledger["last_decision_key"] = None
        if fresh:
            ledger["pending_resolution"] = {
                "gap_id": gap_id, "from_revision": current,
                "decision_digest": decision_key,
            }
            ledger["last_decision_key"] = decision_key
        else:
            ledger["pending_resolution"] = None
        applied_decision = ""
        if fresh:
            pending_gap = next(gap for gap in ledger["unresolved_gaps"] if gap["gap_id"] == gap_id)
            if decision.isdecimal() and not 1 <= int(decision) <= len(pending_gap["options"]):
                fail("Choose a listed option or supply a custom rule in words")
            if decision.isdecimal() and 1 <= int(decision) <= len(pending_gap["options"]):
                answer = pending_gap["options"][int(decision) - 1]
            elif decision.startswith(f"{gap_id}:"):
                answer = decision[len(gap_id) + 1:].strip()
            else:
                answer = decision
            if not answer:
                fail("A product decision answer is required")
            applied_decision = f"{gap_id}: {answer}"
        save_json(ledger_path, ledger)
        return {"prd_revision": current, "decision": applied_decision,
                "comment": inputs.get("prd_comment", "") if fresh else ""}

    if stage == "start_review":
        ledger["review_start_revision"] = current
        receipt_path.unlink(missing_ok=True)
        save_json(ledger_path, ledger)
        return {"prd_revision": current}

    if stage == "record":
        if ledger.get("review_start_revision") != current:
            fail("Canonical PRD changed during review; repeat a full review")
        if not receipt_path.is_file():
            fail("Structured PRD review submission is missing")
        submission = read_json(receipt_path)
        verdict = submission.get("verdict")
        if verdict not in ("CLEAN", "PRODUCT_GAP"):
            fail("Review verdict must be CLEAN or PRODUCT_GAP")
        submitted_gaps = submission.get("gaps")
        if not isinstance(submitted_gaps, list):
            fail("Review gaps must be a list")
        gaps = [gap_from_submission(item) for item in submitted_gaps]
        for gap in gaps:
            validate_human_fields(gap, run_id)
        if (verdict == "CLEAN") != (len(gaps) == 0):
            fail("Review verdict and gap list disagree")
        for gap in gaps:
            match = next((old for old in ledger["unresolved_gaps"]
                          if old["gap_id"] == gap["gap_id"] or
                          question_key(old["question"]) == question_key(gap["question"])), None)
            if match:
                gap["gap_id"] = match["gap_id"]
        if len({gap["gap_id"] for gap in gaps}) != len(gaps):
            fail("Review contains duplicate gap IDs")
        pending = ledger.get("pending_resolution")
        previous_revision = ledger["reviews"][-1]["prd_revision"] if ledger["reviews"] else None
        changed_with_decision = bool(pending and pending["from_revision"] == previous_revision and current != previous_revision)
        discovered_ids = {gap["gap_id"] for gap in gaps}
        if changed_with_decision and pending["gap_id"] not in discovered_ids:
            for old in list(ledger["unresolved_gaps"]):
                if old["gap_id"] == pending["gap_id"]:
                    old["status"] = "resolved"
                    old["resolved_on_revision"] = current
                    old["resolution_decision_digest"] = pending["decision_digest"]
                    ledger["resolved_gaps"].append(old)
                    ledger["unresolved_gaps"].remove(old)
        for gap in gaps:
            if not any(old["gap_id"] == gap["gap_id"] for old in ledger["unresolved_gaps"]):
                ledger["unresolved_gaps"].append({
                    **gap, "discovered_on_revision": current, "status": "unresolved"
                })
        # A CLEAN claim never clears gaps on the same revision, nor gaps that
        # lack an explicit, PRD-changing resolution candidate.
        effective = "PRODUCT_GAP" if ledger["unresolved_gaps"] else verdict
        review = {"sequence": len(ledger["reviews"]) + 1,
                  "prd_revision": current, "submitted_verdict": verdict,
                  "effective_verdict": effective,
                  "discovered_gap_ids": sorted(discovered_ids)}
        ledger["reviews"].append(review)
        ledger["approval"] = None
        ledger["pending_resolution"] = None
        ledger["pending_gap_id"] = ledger["unresolved_gaps"][0]["gap_id"] if ledger["unresolved_gaps"] else None
        save_json(ledger_path, ledger)
        message = gap_message(ledger["unresolved_gaps"][0]) if effective == "PRODUCT_GAP" else approval_message()
        return {"effective_verdict": effective, "can_approve": effective == "CLEAN",
                "prd_revision": current, "human_message": message,
                "unresolved_gap_ids": [gap["gap_id"] for gap in ledger["unresolved_gaps"]]}

    if stage == "verify":
        last = ledger["reviews"][-1] if ledger["reviews"] else None
        if not last or last["effective_verdict"] != "CLEAN" or ledger["unresolved_gaps"]:
            fail("PRD approval blocked: unresolved PRODUCT GAP")
        if current != last["prd_revision"]:
            fail("PRD approval blocked: canonical PRD changed after review")
        state = read_json(run_dir / "state.json")
        gate = state["step_results"].get("prd-governance-gate", {})
        if gate.get("output", {}).get("choice") != "approve":
            fail("PRD approval blocked: no explicit Approve choice")
        # The input is presented before replay; it is bound to the review
        # visible at that earlier pause. Interactive choice occurs now.
        if inputs.get("prd_gate_decision") == "approve" and ledger.get("approval_request_revision") != current:
            fail("PRD approval blocked: approval belongs to another PRD revision")
        ledger["approval"] = {"approved_prd_revision": current,
                              "review_sequence": last["sequence"], "choice": "approve"}
        save_json(ledger_path, ledger)
        return {"approved_prd_revision": current, "review_sequence": last["sequence"]}

    fail(f"Unknown governance stage: {stage}")


if __name__ == "__main__":
    try:
        print(json.dumps(main(sys.argv[1], sys.argv[2]), ensure_ascii=False))
    except (KeyError, IndexError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PRD governance validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
