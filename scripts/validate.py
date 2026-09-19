"""Validate the distributable skill and local documentation links."""

from __future__ import annotations

import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate_skill(skill: Path) -> list[str]:
    errors = []
    required = ["SKILL.md", "agents/openai.yaml", "LICENSE"]
    for name in required:
        if not (skill / name).is_file():
            errors.append(f"missing skill file: {name}")
    if errors:
        return errors
    for path in skill.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink in distributable: {path.name}")
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return errors + ["SKILL.md needs YAML frontmatter bounded by exact --- lines"]
    try:
        metadata = yaml.safe_load(match[1])
        ui = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return errors + [f"invalid YAML: {exc}"]
    if not isinstance(metadata, dict):
        return errors + ["frontmatter must be a mapping"]
    if metadata.get("name") != "solo-operator":
        errors.append("skill name must be solo-operator")
    description = metadata.get("description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append("description must contain 1–1024 characters")
    if not text[match.end():].strip():
        errors.append("skill body is empty")
    if re.search(r"\[TODO:[^\]]*\]", text):
        errors.append("unfinished scaffold placeholder")
    if not isinstance(ui, dict) or not isinstance(ui.get("interface"), dict):
        return errors + ["openai.yaml must define interface metadata"]
    interface = ui["interface"]
    for key in ["display_name", "short_description", "default_prompt"]:
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            errors.append(f"invalid interface.{key}")
    if not 25 <= len(str(interface.get("short_description", ""))) <= 64:
        errors.append("short_description must contain 25–64 characters")
    if "$solo-operator" not in str(interface.get("default_prompt", "")):
        errors.append("default_prompt must invoke $solo-operator")
    policy = ui.get("policy", {})
    if not isinstance(policy, dict) or policy.get("allow_implicit_invocation", True) is not True:
        errors.append("automatic selection must remain enabled")
    return errors


def validate_links(root: Path) -> list[str]:
    errors = []
    # Raw responses are immutable evidence, not authored documentation.
    docs = [p for p in root.rglob("*.md") if ".git" not in p.parts and "results" not in p.parts]
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        text = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", text)
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", text):
            url = urlsplit(target.strip("<>"))
            if url.scheme or url.netloc or not url.path:
                continue
            destination = (doc.parent / unquote(url.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f"broken or escaping local link in {doc.relative_to(root)}: {target}")
    return errors


def validate_repo(root: Path) -> list[str]:
    errors = validate_skill(root / "skills/solo-operator")
    for name in ["README.md", "LICENSE", "CONTRIBUTING.md", "requirements-dev.txt",
                 ".github/workflows/validate.yml", "evals/cases.json", "evals/RUBRIC.md",
                 "evals/REPORT.md", "evals/SIMPLE_SCORECARD.json", "evals/SIMPLE_REPORT.md",
                 "docs/releases/v0.1.0.md"]:
        if not (root / name).is_file():
            errors.append(f"missing repository file: {name}")
    packaged_license = root / "skills/solo-operator/LICENSE"
    if packaged_license.exists() and (root / "LICENSE").exists():
        if packaged_license.read_bytes() != (root / "LICENSE").read_bytes():
            errors.append("packaged MIT license differs from root LICENSE")
    try:
        cases = json.loads((root / "evals/cases.json").read_text(encoding="utf-8"))
        ids = [case["id"] for case in cases]
        if len(ids) != 8 or len(set(ids)) != len(ids):
            errors.append("expected eight distinct behavioral cases")
        for case in cases:
            if not case.get("prompt") or not case.get("checks"):
                errors.append("each behavioral case needs a prompt and review checks")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"invalid behavioral cases: {exc}")
    return errors + validate_links(root)


if __name__ == "__main__":
    problems = validate_repo(ROOT)
    for problem in problems:
        print(f"FAIL: {problem}")
    print(f"Package validation: {'FAIL' if problems else 'PASS'}")
    raise SystemExit(bool(problems))
