"""Render a small, deterministic scorecard from the published behavioral run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARMS = ("baseline", "skill")
SCORE_KEYS = ("evidence", "uncertainty", "experiment", "founder_fit", "decision")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON scorecard {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("scorecard must be a JSON object")
    return value


def validate_scorecard(data: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    source_run = data.get("source_run")
    if not isinstance(source_run, str) or not source_run:
        errors.append("source_run must be a non-empty string")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["cases must be a non-empty list"]
    ids: list[str] = []
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{prefix}.id must be a non-empty string")
            continue
        ids.append(case_id)
        if not isinstance(case.get("title"), str) or not case["title"].strip():
            errors.append(f"{prefix}.title must be a non-empty string")
        for arm in ARMS:
            scores = case.get(arm)
            if not isinstance(scores, dict):
                errors.append(f"{prefix}.{arm} must be an object")
                continue
            for key in SCORE_KEYS:
                value = scores.get(key)
                if not isinstance(value, int) or isinstance(value, bool) or value not in (0, 1, 2):
                    errors.append(f"{prefix}.{arm}.{key} must be 0, 1, or 2")
            response = root / "evals" / "results" / str(source_run) / arm / case_id / "response.md"
            if not response.is_file():
                errors.append(f"missing raw response: {response}")
    if len(ids) != len(set(ids)):
        errors.append("case IDs must be unique")
    return errors


def flags(scores: dict[str, int]) -> dict[str, bool]:
    """Turn the original 0–2 dimensions into three plain-language checks."""
    return {
        "evidence": scores["evidence"] == 2 and scores["uncertainty"] == 2,
        "experiment": scores["experiment"] == 2 and scores["founder_fit"] == 2,
        "decision": scores["decision"] == 2,
    }


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    cases = data["cases"]
    summary: dict[str, Any] = {"cases": len(cases), "arms": {}}
    for arm in ARMS:
        counts = {name: 0 for name in ("evidence", "experiment", "decision", "all_three")}
        total = 0
        for case in cases:
            scores = case[arm]
            checks = flags(scores)
            for name in ("evidence", "experiment", "decision"):
                counts[name] += int(checks[name])
            counts["all_three"] += int(all(checks.values()))
            total += sum(scores.values())
        summary["arms"][arm] = {
            "counts": counts,
            "total_score": total,
            "mean_score": total / len(cases),
        }
    return summary


def mark(value: bool) -> str:
    return "✅" if value else "—"


def pct(count: int, total: int) -> str:
    return f"{count}/{total} ({count / total:.0%})"


def render_report(data: dict[str, Any]) -> str:
    summary = summarize(data)
    total = summary["cases"]
    baseline = summary["arms"]["baseline"]
    skill = summary["arms"]["skill"]
    lines = [
        "# Simple scorecard — Solo Operator",
        "",
        f"> **Result:** the skill improved the number of cases with a strong, founder-fit experiment from **{baseline['counts']['experiment']}/{total}** to **{skill['counts']['experiment']}/{total}**. Evidence handling was already strong without the skill, and the skill had one decision-focus regression in the idea-sprawl case.",
        "",
        "This is a plain-language secondary summary of the published `2026-09-19-v0.1.0` run. It reuses the original five dimension scores; it does not make another model call.",
        "",
        "## The three questions",
        "",
        "| Simple question | No skill | With skill | Change |",
        "| --- | ---: | ---: | ---: |",
        f"| Can it separate evidence from uncertainty? | {pct(baseline['counts']['evidence'], total)} | {pct(skill['counts']['evidence'], total)} | {skill['counts']['evidence'] - baseline['counts']['evidence']:+d} case |",
        f"| Does it propose a bounded test that fits the founder? | {pct(baseline['counts']['experiment'], total)} | {pct(skill['counts']['experiment'], total)} | {skill['counts']['experiment'] - baseline['counts']['experiment']:+d} cases |",
        f"| Does the decision follow the evidence? | {pct(baseline['counts']['decision'], total)} | {pct(skill['counts']['decision'], total)} | {skill['counts']['decision'] - baseline['counts']['decision']:+d} case |",
        f"| All three in the same answer | {pct(baseline['counts']['all_three'], total)} | {pct(skill['counts']['all_three'], total)} | {skill['counts']['all_three'] - baseline['counts']['all_three']:+d} cases |",
        "",
        "The original five-point review averaged **{:.3f}/10** without the skill and **{:.3f}/10** with it. Both arms passed all eight cases under the original pass rule.".format(baseline["mean_score"], skill["mean_score"]),
        "",
        "## Case-by-case view",
        "",
        "`E` = evidence separated, `T` = bounded founder-fit test, `D` = decision follows evidence.",
        "",
        "| Case | No skill (E/T/D) | With skill (E/T/D) | Raw answers |",
        "| --- | --- | --- | --- |",
    ]
    for case in data["cases"]:
        baseline_flags = flags(case["baseline"])
        skill_flags = flags(case["skill"])
        baseline_marks = "/".join(mark(baseline_flags[name]) for name in ("evidence", "experiment", "decision"))
        skill_marks = "/".join(mark(skill_flags[name]) for name in ("evidence", "experiment", "decision"))
        raw = f"[baseline](results/{data['source_run']}/baseline/{case['id']}/response.md) · [skill](results/{data['source_run']}/skill/{case['id']}/response.md)"
        lines.append(f"| {case['title']} | {baseline_marks} | {skill_marks} | {raw} |")
    lines.extend([
        "",
        "## Two concrete examples",
        "",
    ])
    for example in data.get("examples", []):
        case_id = example["case_id"]
        lines.extend([
            f"### {example['title']}",
            "",
            f"- **No skill:** “{example['baseline_quote']}”",
            f"- **With skill:** “{example['skill_quote']}”",
            f"- [Read the full baseline response](results/{data['source_run']}/baseline/{case_id}/response.md) · [Read the full skill response](results/{data['source_run']}/skill/{case_id}/response.md)",
            "",
        ])
    lines.extend([
        "## How to read this",
        "",
        "The clearest positive signal is experiment design: the skill more often adds an explicit time, workload, price, or continuation cap. It does not create a new evidence advantage here because the baseline already handled the evidence cases well. The idea-sprawl answer also shows a real tradeoff: the skill followed the request for 30 ideas, but that diluted the immediate decision, so the decision check is marked as not strong.",
        "",
        "## Limits",
        "",
        "- The scorecard is a deterministic re-analysis of one sample per case, not a new benchmark.",
        "- The underlying scores are the same unblinded qualitative AI review by the authoring assistant; they were not independently rescored for this page.",
        "- The eight cases are synthetic, and both arms passed the original threshold. This does not establish statistical superiority, real customer outcomes, or profitability.",
        "- The simple checks are intentionally easy to understand; they should be followed by repeated, blinded evaluation before making a stronger claim.",
        "",
        "Source: [full report](REPORT.md) · [rubric](RUBRIC.md) · [reproduction guide](README.md)",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scorecard", type=Path, default=ROOT / "evals/SIMPLE_SCORECARD.json")
    parser.add_argument("--out", type=Path, default=ROOT / "evals/SIMPLE_REPORT.md")
    args = parser.parse_args()
    data = load_json(args.scorecard)
    errors = validate_scorecard(data, ROOT)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    args.out.write_text(render_report(data), encoding="utf-8")
    summary = summarize(data)
    print(
        "Simple scorecard: "
        f"experiment {summary['arms']['baseline']['counts']['experiment']}/{summary['cases']} -> "
        f"{summary['arms']['skill']['counts']['experiment']}/{summary['cases']}; "
        f"all three {summary['arms']['baseline']['counts']['all_three']}/{summary['cases']} -> "
        f"{summary['arms']['skill']['counts']['all_three']}/{summary['cases']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
