#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from io import BytesIO


REPO = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Artifact:
    target: Path
    source: Path
    source_id: str
    revision: str


def run(*args: str, cwd: Path | None = None, capture: bool = False) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout.strip() if capture else ""


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    if path.is_file():
        hasher.update(path.read_bytes())
        return hasher.hexdigest()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        hasher.update(item.relative_to(path).as_posix().encode())
        hasher.update(b"\0")
        hasher.update(item.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def copy_path(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{target.name}.", dir=target.parent)) / "value"
    if source.is_dir():
        shutil.copytree(source, staging, symlinks=True)
    else:
        shutil.copy2(source, staging)
    remove_path(target)
    staging.replace(target)
    staging.parent.rmdir()


def matching(target: Path, source: Path, mode: str) -> bool:
    if mode == "link":
        return target.is_symlink() and target.resolve(strict=False) == source.resolve()
    if not os.path.lexists(target):
        return False
    if target.is_symlink() or target.is_dir() != source.is_dir():
        return False
    return digest(target) == digest(source)


def render(template: Path, prompt: Path) -> str:
    marker = "{{PROMPT_BODY}}"
    text = template.read_text()
    if text.count(marker) != 1:
        raise RuntimeError(f"template must contain one {marker}: {template}")
    return text.replace(marker, prompt.read_text().rstrip())


def materialize_external(source: dict[str, str], cache: Path, dry_run: bool) -> Path | None:
    name = source["name"]
    commit = source["commit"]
    target = cache / "skills" / name / commit
    if (target / "SKILL.md").is_file():
        return target
    if dry_run:
        print(f"FETCH   {name} at {commit[:12]}")
        return None

    repo_key = hashlib.sha256(source["url"].encode()).hexdigest()[:16]
    mirror = cache / "repos" / f"{repo_key}.git"
    mirror.parent.mkdir(parents=True, exist_ok=True)
    if not mirror.exists():
        run("git", "clone", "--bare", "--filter=blob:none", source["url"], str(mirror))
    try:
        run("git", "cat-file", "-e", f"{commit}^{{commit}}", cwd=mirror)
    except subprocess.CalledProcessError:
        run("git", "fetch", "--no-tags", "origin", commit, cwd=mirror)

    archive_args = ["git", "archive", commit]
    if source["path"] != ".":
        archive_args.append(source["path"])
    archive = subprocess.run(archive_args, cwd=mirror, check=True, stdout=subprocess.PIPE).stdout
    target.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f".{name}.", dir=target.parent))
    with tarfile.open(fileobj=BytesIO(archive)) as bundle:
        bundle.extractall(work, filter="data")
    extracted = work if source["path"] == "." else work / source["path"]
    shutil.copytree(extracted, target)
    shutil.rmtree(work)
    if not (target / "SKILL.md").is_file():
        raise RuntimeError(f"locked source has no SKILL.md: {name}")
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install unified Codex and OpenCode configuration.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--link", action="store_const", const="link", dest="mode")
    mode.add_argument("--copy", action="store_const", const="copy", dest="mode")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--exclude", action="append", default=[], metavar="SKILL")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.force and args.mode != "copy":
        parser.error("--force is supported only with --copy")
    return args


def require_writable(path: Path, label: str) -> None:
    probe = path
    while not probe.exists():
        if probe.parent == probe:
            raise RuntimeError(f"cannot resolve a writable parent for {label}: {path}")
        probe = probe.parent
    if not os.access(probe, os.W_OK | os.X_OK):
        raise RuntimeError(f"{label} is not writable: {probe}")


def main() -> int:
    args = parse_args()
    user_home = Path.home()
    codex_home = Path(os.environ.get("AGENTS_CONFIG_CODEX_HOME", user_home / ".codex")).expanduser()
    opencode_home = Path(os.environ.get("AGENTS_CONFIG_OPENCODE_HOME", user_home / ".config/opencode")).expanduser()
    shared_home = Path(os.environ.get("AGENTS_CONFIG_SHARED_HOME", user_home / ".agents")).expanduser()
    state_home = Path(os.environ.get("AGENTS_CONFIG_STATE_HOME", user_home / ".local/state/agents-config")).expanduser()
    backup_home = Path(os.environ.get("AGENTS_CONFIG_BACKUP_HOME", user_home / ".agents-config-backups")).expanduser()
    state_file = state_home / "install-state.json"
    require_writable(codex_home, "Codex home")
    require_writable(opencode_home, "OpenCode home")
    require_writable(shared_home, "shared agent home")
    require_writable(state_home, "installer state home")
    require_writable(backup_home, "backup home")
    lock = json.loads((REPO / "skills/sources.lock.json").read_text())
    exclusions = set(args.exclude)

    owned: dict[str, Path] = {}
    for skill_file in sorted((REPO / "skills").glob("*/*/SKILL.md")):
        name = skill_file.parent.name
        if name in owned:
            raise RuntimeError(f"duplicate owned skill directory: {name}")
        owned[name] = skill_file.parent

    externals = {item["name"]: item for item in lock["sources"]}
    duplicates = set(owned) & set(externals)
    if duplicates:
        raise RuntimeError(f"skills are both owned and external: {', '.join(sorted(duplicates))}")
    known = set(owned) | set(externals)
    unknown_exclusions = exclusions - known
    if unknown_exclusions:
        raise RuntimeError(f"unknown excluded skill: {', '.join(sorted(unknown_exclusions))}")

    revision = run("git", "rev-parse", "HEAD", cwd=REPO, capture=True)
    artifacts: list[Artifact] = [
        Artifact(codex_home / "AGENTS.md", REPO / "AGENTS.md", "global-prompt", revision),
        Artifact(opencode_home / "AGENTS.md", REPO / "AGENTS.md", "global-prompt", revision),
        Artifact(opencode_home / "opencode.jsonc", REPO / "harnesses/opencode/opencode.jsonc", "opencode-config", revision),
        Artifact(opencode_home / "agents/computer-use.md", REPO / "harnesses/opencode/agents/computer-use.md", "opencode-computer-use", revision),
    ]

    rendered_sources: list[tuple[Path, str]] = [
        (
            state_home / "rendered/codex/adversarial-reviewer.toml",
            render(REPO / "harnesses/codex/agents/adversarial-reviewer.toml.tmpl", REPO / "agents/adversarial-reviewer.md"),
        ),
        (
            state_home / "rendered/opencode/adversarial-reviewer.md",
            render(REPO / "harnesses/opencode/agents/adversarial-reviewer.md.tmpl", REPO / "agents/adversarial-reviewer.md"),
        ),
    ]
    if not args.dry_run:
        for rendered_path, content in rendered_sources:
            rendered_path.parent.mkdir(parents=True, exist_ok=True)
            rendered_path.write_text(content)
    artifacts.extend(
        [
            Artifact(codex_home / "agents/adversarial-reviewer.toml", rendered_sources[0][0], "adversarial-reviewer", revision),
            Artifact(opencode_home / "agents/adversarial-reviewer.md", rendered_sources[1][0], "adversarial-reviewer", revision),
        ]
    )

    for name, source in owned.items():
        if name not in exclusions:
            artifacts.append(Artifact(shared_home / "skills" / name, source, f"owned-skill:{name}", revision))
    for name, source in externals.items():
        if name in exclusions:
            continue
        materialized = materialize_external(source, state_home / "cache", args.dry_run)
        if materialized is not None:
            artifacts.append(Artifact(shared_home / "skills" / name, materialized, f"external-skill:{name}", source["commit"]))
        else:
            print(f"INSTALL {shared_home / 'skills' / name}")

    previous = {entry["target"]: entry for entry in json.loads(state_file.read_text()).get("targets", [])} if state_file.exists() else {}
    desired_targets = {str(item.target) for item in artifacts}
    changes = 0
    backup_dir: Path | None = None

    for old_target in sorted(set(previous) - desired_targets):
        target = Path(old_target)
        if os.path.lexists(target):
            print(f"REMOVE  {target}")
            changes += 1
            if not args.dry_run:
                remove_path(target)

    state_targets = []
    for item in artifacts:
        if not item.source.exists():
            if args.dry_run:
                continue
            raise RuntimeError(f"missing installation source: {item.source}")
        item_hash = digest(item.source)
        state_targets.append(
            {
                "target": str(item.target),
                "source": item.source_id,
                "revision": item.revision,
                "mode": args.mode,
                "sha256": item_hash,
            }
        )
        if matching(item.target, item.source, args.mode):
            print(f"OK      {item.target}")
            continue
        managed = str(item.target) in previous
        if os.path.lexists(item.target) and not managed and not args.force:
            raise RuntimeError(f"unmanaged destination exists, use --copy --force to back it up: {item.target}")
        print(f"UPDATE  {item.target}" if os.path.lexists(item.target) else f"INSTALL {item.target}")
        changes += 1
        if args.dry_run:
            continue
        if os.path.lexists(item.target) and not managed:
            if backup_dir is None:
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                backup_dir = backup_home / stamp / "unmanaged-collisions"
            backup_target = backup_dir / str(item.target).lstrip("/")
            backup_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(item.target, backup_target)
            print(f"BACKUP  {backup_target}")
        if args.mode == "link":
            remove_path(item.target)
            item.target.parent.mkdir(parents=True, exist_ok=True)
            item.target.symlink_to(item.source)
        else:
            copy_path(item.source, item.target)

    if args.dry_run:
        print(f"DRY RUN {changes} filesystem change(s)")
        return 0

    state_home.mkdir(parents=True, exist_ok=True)
    state = {
        "schema": 1,
        "repository": str(REPO),
        "repository_revision": revision,
        "mode": args.mode,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "exclusions": sorted(exclusions),
        "targets": sorted(state_targets, key=lambda entry: entry["target"]),
    }
    state_file.write_text(json.dumps(state, indent=2) + "\n")
    print(f"DONE    {changes} filesystem change(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR   {error}", file=sys.stderr)
        raise SystemExit(1)
