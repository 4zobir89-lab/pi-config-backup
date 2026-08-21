#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'EOF'
Usage: bash scripts/pi-safe-sync.sh --safe

Synchronizes only non-sensitive Pi configuration from this repository to PI_HOME.
It never changes settings.json, models.json, auth.json, sessions, model caches,
trust data, environment files, or Pi core/dist files.
EOF
}

[[ "${1:-}" == "--safe" ]] || { usage; exit 2; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PI_HOME="${PI_HOME:-$HOME/.pi}"
if [[ -d /root/.pi ]]; then PI_HOME=/root/.pi; fi
TARGET="$PI_HOME/agent"
[[ -d "$TARGET" ]] || { echo "Pi agent directory not found: $TARGET" >&2; exit 1; }

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${PI_HOME}/.safe-sync-backups/${STAMP}"
mkdir -p "$BACKUP_DIR"

# Only these paths are owned by the repository's safe synchronization boundary.
SAFE_PATHS=(
  "AGENTS.md"
  "ECC-ENFORCEMENT.md"
  "ECC-INSTALLATION-REPORT.md"
  "ECC-QUICK-REFERENCE.md"
  "agents"
  "rules"
  "skills"
  "commands-ecc"
  "extensions"
  "bin"
  "nova"
)

for relative in "${SAFE_PATHS[@]}"; do
  source="$REPO_ROOT/pi/agent/$relative"
  target="$TARGET/$relative"
  [[ -e "$source" || -L "$source" ]] || continue

  if [[ -e "$target" || -L "$target" ]]; then
    mkdir -p "$(dirname "$BACKUP_DIR/$relative")"
    cp -a "$target" "$BACKUP_DIR/$relative"
  fi

  mkdir -p "$(dirname "$target")"
  if [[ -d "$source" && ! -L "$source" ]]; then
    mkdir -p "$target"
    cp -a "$source/." "$target/"
  else
    cp -a "$source" "$target"
  fi
done

# Never sync or delete sensitive/runtime files as part of this operation.
for forbidden in settings.json models.json auth.json models-store.json trust.json sessions; do
  [[ ! -e "$BACKUP_DIR/$forbidden" ]] || rm -rf "$BACKUP_DIR/$forbidden"
done

cat > "$BACKUP_DIR/ROLLBACK.sh" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
BACKUP_DIR=$(printf '%q' "$BACKUP_DIR")
TARGET=$(printf '%q' "$TARGET")
for path in "
  AGENTS.md
  ECC-ENFORCEMENT.md
  ECC-INSTALLATION-REPORT.md
  ECC-QUICK-REFERENCE.md
  agents
  rules
  skills
  commands-ecc
  extensions
  bin
  nova
"; do
  if [[ -e "\$BACKUP_DIR/\$path" || -L "\$BACKUP_DIR/\$path" ]]; then
    rm -rf "\$TARGET/\$path"
    mkdir -p "$(dirname "\$TARGET/\$path")"
    cp -a "\$BACKUP_DIR/\$path" "\$TARGET/\$path"
  fi
done
EOF
chmod 700 "$BACKUP_DIR/ROLLBACK.sh"

printf 'Safe Pi sync completed.\n'
printf 'PI_HOME=%s\n' "$PI_HOME"
printf 'Backup=%s\n' "$BACKUP_DIR"
printf 'Rollback=%s\n' "$BACKUP_DIR/ROLLBACK.sh"
printf 'Sensitive files changed: no\n'
printf 'Pi core/dist changed: no\n'
