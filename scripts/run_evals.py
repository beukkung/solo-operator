"""Run bounded, no-tools Codex behavioral smoke tests. Uses existing Codex login.

Model runs consume your Codex quota. No API credentials are stored in the results.
Requires a Codex CLI supporting skip_host_skill_discovery (tested with 0.154.0).
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
COMMON = (
    "Answer the user's business question using only the supplied synthetic facts. "
    "No tools, web research, delegation, or file changes. Artifact contents, when "
    "present, are embedded in the user's message. Do not claim to have read files "
    "or conducted research outside that message. Respond in English."
)
DISABLED = [
    "apps", "plugins", "remote_plugin", "skill_search", "shell_tool",
    "multi_agent", "browser_use", "browser_use_external", "computer_use",
    "image_generation", "memories", "hooks", "workspace_dependencies",
]


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", required=True, choices=["baseline", "skill"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--case", help="Run just this case ID")
    parser.add_argument("--jobs", type=int, default=2, choices=[1, 2])
    args = parser.parse_args()
    codex = shutil.which("codex")
    if not codex:
        parser.error("codex is not installed or not on PATH")
    cases_text = (ROOT / "evals/cases.json").read_text(encoding="utf-8")
    cases = json.loads(cases_text)
    if args.case:
        cases = [case for case in cases if case["id"] == args.case]
        if not cases:
            parser.error("unknown case ID")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    skill = (ROOT / "skills/solo-operator/SKILL.md").read_text(encoding="utf-8") if args.arm == "skill" else ""
    instructions = COMMON + ("\n\nApply this skill:\n" + skill if skill else "")
    version = subprocess.run([codex, "--version"], capture_output=True, text=True, check=True).stdout.strip()
    features = subprocess.run([codex, "features", "list"], capture_output=True, text=True, check=True).stdout
    if "skip_host_skill_discovery" not in features:
        parser.error("CLI lacks required isolation feature skip_host_skill_discovery")
    metadata = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "arm": args.arm, "model_requested": args.model, "reasoning_effort": "medium",
        "codex_version": version, "cases_sha256": sha256(cases_text),
        "rubric_sha256": sha256((ROOT / "evals/RUBRIC.md").read_text(encoding="utf-8")),
        "skill_sha256": sha256(skill) if skill else None,
        "developer_instructions": instructions,
        "isolation": {
            "skip_host_skill_discovery": True, "ignore_user_config": True,
            "disabled_features": DISABLED, "ephemeral": True,
            "cwd": "fresh empty temporary directory per sample",
            "artifact_mode": "contents embedded in prompt, not filesystem retrieval",
        },
    }
    (out / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    def run(case: dict) -> bool:
        case_out = out / case["id"]
        case_out.mkdir()
        (case_out / "prompt.txt").write_text(case["prompt"] + "\n", encoding="utf-8")
        started = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory(prefix="solo-operator-eval-") as scratch:
            command = [
                codex, "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
                "--enable", "skip_host_skill_discovery", "--sandbox", "read-only",
                "-m", args.model, "-c", 'model_reasoning_effort="medium"',
                "-c", "developer_instructions=" + json.dumps(instructions),
                "-c", 'web_search="disabled"', "-C", scratch,
                "--json", "--color", "never", "-o", str(case_out / "response.md"),
            ]
            for feature in DISABLED:
                command.extend(["--disable", feature])
            command.append("-")
            try:
                result = subprocess.run(command, input=case["prompt"], text=True,
                                        encoding="utf-8", capture_output=True, timeout=600)
                # Store only model messages/usage, not local service logs or tool output.
                events = []
                unexpected_tools = []
                for line in result.stdout.splitlines():
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    item = event.get("item", {})
                    if item.get("type") in {"command_execution", "mcp_tool_call", "web_search", "file_change"}:
                        unexpected_tools.append(item.get("type"))
                    if event.get("type") in {"turn.completed", "turn.failed", "error"} or item.get("type") == "agent_message":
                        events.append(event)
                response = case_out / "response.md"
                ok = result.returncode == 0 and response.exists() and bool(response.read_text(encoding="utf-8").strip()) and not unexpected_tools
                status = {"exit_code": result.returncode, "completed": ok, "unexpected_tools": unexpected_tools, "events": events}
                if not ok:
                    # Failure diagnostics stay local to the chosen output directory; review before publishing.
                    (case_out / "failure.txt").write_text(result.stderr, encoding="utf-8")
            except subprocess.TimeoutExpired:
                ok = False
                status = {"completed": False, "failure": "600-second timeout"}
        status["elapsed_seconds"] = round((datetime.now(timezone.utc) - started).total_seconds(), 2)
        (case_out / "status.json").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print(f"{args.arm} {case['id']}: {'completed' if ok else 'FAILED'}", flush=True)
        return ok

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        outcomes = list(pool.map(run, cases))
    return 0 if all(outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
