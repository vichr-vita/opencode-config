#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib


REPO = Path(__file__).resolve().parents[2]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS    {message}")


def strip_jsonc(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(^|\s)//.*$", r"\1", text, flags=re.M)


def frontmatter(skill: Path) -> dict[str, str]:
    lines = skill.read_text().splitlines()
    label = str(skill.relative_to(REPO)) if skill.is_relative_to(REPO) else str(skill)
    check(bool(lines) and lines[0] == "---", f"frontmatter starts {label}")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"frontmatter closes {label}") from error
    values: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("'\"")
    check(bool(values.get("name")), f"skill name exists {label}")
    check("description" in values, f"skill description exists {label}")
    return values


def render(template: Path, prompt: Path) -> str:
    marker = "{{PROMPT_BODY}}"
    text = template.read_text()
    check(text.count(marker) == 1, f"one prompt marker in {template.relative_to(REPO)}")
    return text.replace(marker, prompt.read_text().rstrip())


def main() -> int:
    lock = json.loads((REPO / "skills/sources.lock.json").read_text())
    check(lock.get("version") == 1, "external source lock schema")
    external_names: set[str] = set()
    for source in lock["sources"]:
        check(bool(re.fullmatch(r"[0-9a-f]{40}", source["commit"])), f"pinned commit for {source['name']}")
        check(source["name"] not in external_names, f"unique locked skill {source['name']}")
        external_names.add(source["name"])

    owned_names: set[str] = set()
    skill_ids: set[str] = set()
    for skill in sorted((REPO / "skills").glob("*/*/SKILL.md")):
        directory_name = skill.parent.name
        check(directory_name not in owned_names, f"unique owned directory {directory_name}")
        owned_names.add(directory_name)
        values = frontmatter(skill)
        check(values["name"] not in skill_ids, f"unique skill ID {values['name']}")
        skill_ids.add(values["name"])
    check(not (owned_names & external_names), "owned and external names do not overlap")

    opencode = REPO / "harnesses/opencode/opencode.jsonc"
    json.loads(strip_jsonc(opencode.read_text()))
    check(True, "OpenCode JSONC parses")
    prompt = REPO / "agents/adversarial-reviewer.md"
    codex_rendered = render(REPO / "harnesses/codex/agents/adversarial-reviewer.toml.tmpl", prompt)
    opencode_rendered = render(REPO / "harnesses/opencode/agents/adversarial-reviewer.md.tmpl", prompt)
    tomllib.loads(codex_rendered)
    check(True, "Codex reviewer TOML parses")
    check(opencode_rendered.startswith("---\n") and "\n---\n\n" in opencode_rendered, "OpenCode reviewer frontmatter parses")
    subprocess.run(["bash", "-n", REPO / "scripts/install.sh"], check=True)
    subprocess.run(["bash", "-n", REPO / "scripts/cleanup-legacy.sh"], check=True)
    check(True, "shell entry points parse")

    user_home = Path.home()
    codex_home = Path(os.environ.get("AGENTS_CONFIG_CODEX_HOME", user_home / ".codex")).expanduser()
    opencode_home = Path(os.environ.get("AGENTS_CONFIG_OPENCODE_HOME", user_home / ".config/opencode")).expanduser()
    shared_home = Path(os.environ.get("AGENTS_CONFIG_SHARED_HOME", user_home / ".agents")).expanduser()
    state_home = Path(os.environ.get("AGENTS_CONFIG_STATE_HOME", user_home / ".local/state/agents-config")).expanduser()
    state_file = state_home / "install-state.json"
    if not state_file.exists():
        print(f"SKIP    live installation checks, state missing at {state_file}")
        return 0

    state = json.loads(state_file.read_text())
    check(codex_home.joinpath("AGENTS.md").read_bytes() == opencode_home.joinpath("AGENTS.md").read_bytes(), "global prompts are identical")
    check(codex_home.joinpath("agents/adversarial-reviewer.toml").exists(), "Codex reviewer is installed")
    check(opencode_home.joinpath("agents/adversarial-reviewer.md").exists(), "OpenCode reviewer is installed")
    check(opencode_home.joinpath("agents/computer-use.md").exists(), "OpenCode computer-use agent is installed")
    check(not codex_home.joinpath("agents/implementer.toml").exists(), "retired Codex implementer is absent")
    check(not codex_home.joinpath("agents/qa.toml").exists(), "retired Codex QA agent is absent")
    installed_ids: set[str] = set()
    for source in lock["sources"]:
        if source["name"] not in state.get("exclusions", []):
            installed_skill = shared_home / "skills" / source["name"] / "SKILL.md"
            check(installed_skill.exists(), f"external skill is installed {source['name']}")
            values = frontmatter(installed_skill)
            check(values["name"] not in installed_ids, f"unique installed skill ID {values['name']}")
            installed_ids.add(values["name"])
    for name in owned_names:
        if name not in state.get("exclusions", []):
            installed_skill = shared_home / "skills" / name / "SKILL.md"
            check(installed_skill.exists(), f"owned skill is installed {name}")
            values = frontmatter(installed_skill)
            check(values["name"] not in installed_ids, f"unique installed skill ID {values['name']}")
            installed_ids.add(values["name"])

    forbidden_roots = [
        opencode_home / "commands",
        opencode_home / "plugins",
        opencode_home / "skills",
        shared_home / "plugins/babysitter",
    ]
    leftovers = [str(path) for root in forbidden_roots if root.exists() for path in root.rglob("*") if re.search(r"babysitter|caveman", path.name, re.I)]
    check(not leftovers, "retired OpenCode and local plugin registrations are absent")
    print(f"PASS    live state has {len(state['targets'])} managed target(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError, tomllib.TOMLDecodeError, subprocess.CalledProcessError) as error:
        print(f"FAIL    {error}", file=sys.stderr)
        raise SystemExit(1)
