# Unified agent configuration

This repository is the editable source for configuration shared by Codex and OpenCode.

Shared instructions live in `AGENTS.md`. Owned skills live under `skills/` in human-readable categories, while externally maintained skills are pinned in `skills/sources.lock.json`. The installer exposes global skills through the flat `~/.agents/skills` directory and writes only the adapter files each harness understands.

Owned skills are global unless their `SKILL.md` front matter contains a `harnesses` include-list. Harness names are case-insensitive. A restricted skill stays in the regular categorized `skills/` tree and declares its targets like this:

```yaml
---
name: example
description: An example Codex-only skill.
harnesses: [codex]
---
```

Use `[codex]` or `[opencode]` for a restricted skill. `[codex, opencode]` has the same meaning as omitting `harnesses`. The installer puts global skills in `~/.agents/skills`, Codex-only skills in `~/.codex/skills`, and OpenCode-only skills in `~/.config/opencode/skills`.

## Install

Use link mode on a machine where this checkout remains available:

```sh
./scripts/install.sh --link
```

Use copy mode for a self-contained installation:

```sh
./scripts/install.sh --copy
```

Both modes accept repeated `--exclude SKILL` options and `--dry-run`. Copy mode also accepts `--force` when an unmanaged destination should be backed up and replaced.

Run `./scripts/verify.sh` after installation. Set the `AGENTS_CONFIG_*` home variables documented in `scripts/install.sh` to test against temporary directories or install on another machine.

## Managed and local files

The repository manages global instructions, shared skills, the adversarial reviewer, the OpenCode computer-use agent, and OpenCode's model configuration. It does not manage credentials, sessions, caches, databases, Codex UI settings, trusted hashes, or the rest of `~/.codex/config.toml`.

External sources use exact Git commits. Locally authored skills remain in this repository. `skills/provenance.md` records how each source was classified during the migration.

## Legacy cleanup

`./scripts/cleanup-legacy.sh --dry-run` lists the retired Caveman and Babysitter paths. The cleanup script runs the replacement-layout gate itself, then creates a timestamped archive before removing anything. Run `./scripts/verify.sh` afterward for the final acceptance check.
