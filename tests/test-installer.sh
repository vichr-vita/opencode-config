#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fixture="$(mktemp -d /tmp/agents-config-test.XXXXXX)"
export AGENTS_CONFIG_CODEX_HOME="$fixture/codex"
export AGENTS_CONFIG_OPENCODE_HOME="$fixture/opencode"
export AGENTS_CONFIG_SHARED_HOME="$fixture/agents"
export AGENTS_CONFIG_STATE_HOME="$fixture/state"
export AGENTS_CONFIG_BACKUP_HOME="$fixture/backups"

mkdir -p "$AGENTS_CONFIG_CODEX_HOME/agents"
printf 'unmanaged\n' > "$AGENTS_CONFIG_CODEX_HOME/AGENTS.md"

if "$repo_dir/scripts/install.sh" --link >/dev/null 2>&1; then
  echo "installer replaced an unmanaged destination without force" >&2
  exit 1
fi

"$repo_dir/scripts/install.sh" --copy --force
second="$($repo_dir/scripts/install.sh --copy --dry-run)"
grep -q 'DRY RUN 0 filesystem change(s)' <<<"$second"
excluded="$($repo_dir/scripts/install.sh --copy --exclude home-tailscale-network --dry-run)"
grep -q "REMOVE  $AGENTS_CONFIG_SHARED_HOME/skills/home-tailscale-network" <<<"$excluded"
find "$AGENTS_CONFIG_BACKUP_HOME" -path '*/unmanaged-collisions/*/AGENTS.md' -type f | grep -q .
python3 "$repo_dir/tests/test-skill-metadata.py"
"$repo_dir/scripts/verify.sh" >/dev/null
echo "PASS    installer collision, idempotence, and exclusion checks"
