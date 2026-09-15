#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

from skill_metadata import read_skill_frontmatter, skill_harnesses, skill_install_root


REPO = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify unified agent configuration.")
    parser.add_argument(
        "--pre-cleanup",
        action="store_true",
        help="verify the replacement layout without requiring retired files to be absent",
    )
    return parser.parse_args()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS    {message}")


def strip_jsonc(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(^|\s)//.*$", r"\1", text, flags=re.M)


def frontmatter(skill: Path) -> dict[str, str | frozenset[str]]:
    label = str(skill.relative_to(REPO)) if skill.is_relative_to(REPO) else str(skill)
    try:
        values = read_skill_frontmatter(skill)
    except ValueError as error:
        raise AssertionError(str(error)) from error
    check(True, f"frontmatter parses {label}")
    check(bool(values.get("name")), f"skill name exists {label}")
    check("description" in values, f"skill description exists {label}")
    return values


def render(template: Path, prompt: Path) -> str:
    marker = "{{PROMPT_BODY}}"
    text = template.read_text()
    check(text.count(marker) == 1, f"one prompt marker in {template.relative_to(REPO)}")
    return text.replace(marker, prompt.read_text().rstrip())


def main() -> int:
    args = parse_args()
    lock = json.loads((REPO / "skills/sources.lock.json").read_text())
    check(lock.get("version") == 1, "external source lock schema")
    external_names: set[str] = set()
    for source in lock["sources"]:
        check(bool(re.fullmatch(r"[0-9a-f]{40}", source["commit"])), f"pinned commit for {source['name']}")
        check(source["name"] not in external_names, f"unique locked skill {source['name']}")
        external_names.add(source["name"])

    owned_skills: dict[str, Path] = {}
    skill_ids: set[str] = set()
    for skill in sorted((REPO / "skills").glob("*/*/SKILL.md")):
        directory_name = skill.parent.name
        check(directory_name not in owned_skills, f"unique owned directory {directory_name}")
        owned_skills[directory_name] = skill
        values = frontmatter(skill)
        check(values["name"] not in skill_ids, f"unique skill ID {values['name']}")
        skill_ids.add(values["name"])
    check(not (set(owned_skills) & external_names), "owned and external names do not overlap")

    opencode = REPO / "harnesses/opencode/opencode.jsonc"
    json.loads(strip_jsonc(opencode.read_text()))
    check(True, "OpenCode JSONC parses")
    computer_use = REPO / "harnesses/opencode/agents/computer-use.md"
    check("disable: true" not in computer_use.read_text(), "OpenCode computer-use agent is enabled")
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
    if not args.pre_cleanup:
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
    for name, source_skill in owned_skills.items():
        if name not in state.get("exclusions", []):
            install_root = skill_install_root(
                skill_harnesses(source_skill),
                codex_home=codex_home,
                opencode_home=opencode_home,
                shared_home=shared_home,
            )
            installed_skill = install_root / name / "SKILL.md"
            check(installed_skill.exists(), f"owned skill is installed {name}")
            values = frontmatter(installed_skill)
            check(values["name"] not in installed_ids, f"unique installed skill ID {values['name']}")
            installed_ids.add(values["name"])

    if not args.pre_cleanup:
        forbidden_roots = [
            opencode_home / "commands",
            opencode_home / "plugins",
            opencode_home / "skills",
            shared_home / "plugins/babysitter",
        ]
        leftovers = [str(path) for root in forbidden_roots if root.exists() for path in root.rglob("*") if re.search(r"babysitter|caveman", path.name, re.I)]
        check(not leftovers, "retired OpenCode and local plugin registrations are absent")
        if shutil.which("codex") and codex_home == user_home / ".codex":
            marketplace_result = subprocess.run(
                ["codex", "plugin", "marketplace", "list"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            check(not re.search(r"^babysitter\s", marketplace_result.stdout, re.M | re.I), "Babysitter marketplace is absent")
            plugin_result = subprocess.run(
                ["codex", "plugin", "list"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            check(not re.search(r"^babysitter@babysitter\s+installed", plugin_result.stdout, re.M | re.I), "Babysitter plugin is absent")
    print(f"PASS    live state has {len(state['targets'])} managed target(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError, json.JSONDecodeError, tomllib.TOMLDecodeError, subprocess.CalledProcessError) as error:
        print(f"FAIL    {error}", file=sys.stderr)
        raise SystemExit(1)
