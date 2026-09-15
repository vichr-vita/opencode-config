from __future__ import annotations

from pathlib import Path
import re


ALL_HARNESSES = frozenset({"codex", "opencode"})


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _parse_harness_name(value: str, skill: Path) -> str:
    name = _unquote(value).casefold()
    if name not in ALL_HARNESSES:
        supported = ", ".join(sorted(ALL_HARNESSES))
        raise ValueError(f"unsupported harness {value!r} in {skill}; expected one of: {supported}")
    return name


def _parse_harnesses(value: str, following_lines: list[str], skill: Path) -> frozenset[str]:
    if value:
        if not (value.startswith("[") and value.endswith("]")):
            raise ValueError(f"harnesses must be an array in {skill}")
        items = [item.strip() for item in value[1:-1].split(",") if item.strip()]
    else:
        items = []
        for line in following_lines:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            match = re.fullmatch(r"\s+-\s+(.+?)\s*", line)
            if not match:
                break
            items.append(match.group(1))
    harnesses = [_parse_harness_name(item, skill) for item in items]
    if not harnesses:
        raise ValueError(f"harnesses must include at least one harness in {skill}")
    if len(harnesses) != len(set(harnesses)):
        raise ValueError(f"harnesses contains duplicates in {skill}")
    return frozenset(harnesses)


def read_skill_frontmatter(skill: Path) -> dict[str, str | frozenset[str]]:
    lines = skill.read_text().splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"frontmatter does not start in {skill}")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"frontmatter does not close in {skill}") from error

    values: dict[str, str | frozenset[str]] = {}
    for index, line in enumerate(lines[1:end], start=1):
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            continue
        key, raw_value = match.groups()
        if key in values:
            raise ValueError(f"duplicate frontmatter key {key!r} in {skill}")
        if key == "harnesses":
            values[key] = _parse_harnesses(raw_value, lines[index + 1 : end], skill)
        else:
            values[key] = _unquote(raw_value)
    return values


def skill_harnesses(skill: Path) -> frozenset[str]:
    value = read_skill_frontmatter(skill).get("harnesses", ALL_HARNESSES)
    if not isinstance(value, frozenset):
        raise ValueError(f"harnesses must be an array in {skill}")
    return value


def skill_install_root(
    harnesses: frozenset[str],
    *,
    codex_home: Path,
    opencode_home: Path,
    shared_home: Path,
) -> Path:
    if harnesses == ALL_HARNESSES:
        return shared_home / "skills"
    if harnesses == {"codex"}:
        return codex_home / "skills"
    if harnesses == {"opencode"}:
        return opencode_home / "skills"
    raise ValueError(f"unsupported harness selection: {sorted(harnesses)}")
