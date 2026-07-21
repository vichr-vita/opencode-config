# OpenCode Configuration

Portable OpenCode configuration containing agents, commands, plugins, skills,
hooks, and model settings.

## Install On Another Machine

Install Git, Node.js, npm, and OpenCode first. Then clone this repository into
OpenCode's global configuration directory:

```sh
mkdir -p ~/.config
git clone <repository-url> ~/.config/opencode
cd ~/.config/opencode
npm ci
```

If `~/.config/opencode` already exists, move or remove it before cloning.

Authenticate OpenCode providers separately on the new machine. Credentials and
machine-local authentication state are intentionally not stored here.

Quit and restart OpenCode after installation so it loads this configuration.

## Update

```sh
cd ~/.config/opencode
git pull
npm ci
```

## Repository Contents

- `opencode.json`: global OpenCode settings and enabled plugins
- `AGENTS.md`: global agent instructions
- `agents/`: custom subagents
- `commands/`: custom slash commands
- `plugins/`: local OpenCode plugins
- `skills/`: reusable agent skills
- `hooks.json`: hook configuration
- `package.json` and lockfiles: plugin runtime dependencies

Generated dependency directories, runtime markers, backups, and local secret
files are excluded by `.gitignore`.
