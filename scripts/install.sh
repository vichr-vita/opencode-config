#!/usr/bin/env bash
set -euo pipefail

# Override these paths when testing or installing into a non-default home:
# AGENTS_CONFIG_CODEX_HOME, AGENTS_CONFIG_OPENCODE_HOME,
# AGENTS_CONFIG_SHARED_HOME, AGENTS_CONFIG_STATE_HOME, AGENTS_CONFIG_BACKUP_HOME.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$script_dir/lib/install.py" "$@"

