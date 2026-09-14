#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dry_run=0
if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=1
  shift
fi
if [[ "$#" -ne 0 ]]; then
  echo "usage: $0 [--dry-run]" >&2
  exit 2
fi

user_home="${HOME}"
codex_home="${AGENTS_CONFIG_CODEX_HOME:-$user_home/.codex}"
opencode_home="${AGENTS_CONFIG_OPENCODE_HOME:-$user_home/.config/opencode}"
shared_home="${AGENTS_CONFIG_SHARED_HOME:-$user_home/.agents}"
backup_home="${AGENTS_CONFIG_BACKUP_HOME:-$user_home/.agents-config-backups}"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_dir="$backup_home/$stamp/legacy-cleanup"

targets=(
  "$codex_home/agents/implementer.toml"
  "$codex_home/agents/qa.toml"
  "$opencode_home/.caveman-active"
  "$opencode_home/.opencode"
  "$opencode_home/commands"
  "$opencode_home/hooks.json"
  "$opencode_home/marketplace.json"
  "$opencode_home/opencode.json.bak"
  "$opencode_home/package.json"
  "$opencode_home/package-lock.json"
  "$opencode_home/bun.lock"
  "$opencode_home/plugins"
  "$opencode_home/skills"
  "$shared_home/plugins/babysitter"
)

found=0
for target in "${targets[@]}"; do
  if [[ -e "$target" || -L "$target" ]]; then
    found=1
    if [[ "$dry_run" -eq 1 ]]; then
      echo "REMOVE  $target"
      continue
    fi
    relative="${target#/}"
    destination="$backup_dir/$relative"
    mkdir -p "$(dirname "$destination")"
    mv "$target" "$destination"
    echo "BACKUP  $target -> $destination"
  fi
done

if [[ "$dry_run" -eq 1 ]]; then
  command -v codex >/dev/null && codex plugin list 2>/dev/null | grep -Ei 'babysitter|caveman' || true
  [[ "$found" -eq 1 ]] || echo "NOOP    no legacy paths found"
  exit 0
fi

"$script_dir/verify.sh" --pre-cleanup >/dev/null

if command -v codex >/dev/null && [[ "$codex_home" == "$user_home/.codex" ]]; then
  if codex plugin list 2>/dev/null | grep -q '^babysitter@babysitter .*installed'; then
    codex plugin remove babysitter@babysitter --json
  fi
  if codex plugin marketplace list 2>/dev/null | grep -q 'Marketplace `babysitter`'; then
    codex plugin marketplace remove babysitter
  fi
fi

echo "DONE    legacy material moved to $backup_dir"
