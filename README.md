# pi-config-backup

Backup of the Pi agent's internal instructions, rules, skills, and current settings.

- **Owner:** 4zobir89-lab
- **Visibility:** PRIVATE
- **Purpose:** version-control Pi/ECC config so it can be edited and updated over time.

## Structure

```
pi-config-backup/
├── pi/        # mirror of /root/.pi  (Pi agent config: AGENTS.md, ECC rules, settings, skills, prompts, mcp, penpot-mcp, ...)
└── ecc/       # mirror of /root/ecc-repo  (the ECC bundle: skills, commands, hooks, docs, scripts, dotfiles)
```

### What is included
- `pi/agent/AGENTS.md`, `ECC-*.md` — core instructions
- `pi/agent/settings.json`, `pi/agent/models.json`, `pi/mcp.json` — current agent settings
- `pi/agent/rules/`, `pi/agent/agents/`, `pi/agent/commands-ecc/`, `pi/agent/extensions/`, `pi/agent/bin/`
- `pi/agent/skills/`, `pi/skills/` — installed skills
- `pi/prompts-lib/`, `pi/penpot-mcp/`
- `ecc/` — full ECC bundle (skills, commands, hooks, docs, scripts, dotfiles)

### What was EXCLUDED (for safety / not config)
- `pi/agent/auth.json` — gh session credentials
- `pi/agent/sessions/` — chat history
- `pi/agent/models-store.json` — cached provider keys
- `pi/agent/.backup-*` — old backups
- `pi/agent/ecc-*` — symlinks (ecc content is mirrored under `ecc/`)
- all `node_modules/` — installable deps (reinstall instead of committing)
- `.env` / `.env.*` — secret env files
- any `.git/` directories

## ⚠️ Secrets note
`pi/agent/settings.json` and `pi/agent/models.json` contain **real API keys**
(e.g. `fe_oa_...`, `dahl_...`). The repo is PRIVATE, but:
- Never make this repo public without redacting those values first.
- Prefer env-var references (like the existing `$NVIDIA_API_KEY`) over hardcoded keys.

## Restore
```bash
# Pi config
rsync -a --delete pi/ /root/.pi/
# ECC bundle
rsync -a --delete ecc/ /root/ecc-repo/
# then reinstall deps where needed, e.g.:
cd /root/.pi/penpot-mcp && npm install
```
Use with care: review changes before overwriting live config.

## Update workflow
```bash
cd /root/pi-config-backup
git add -A && git commit -m "chore: update pi config" && git push
```
