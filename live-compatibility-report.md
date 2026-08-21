# Live Compatibility Report — Nova layer on Pi (live)

- **Date:** 2026-08-21
- **Scope:** Verification only. No change to `models.json`, `defaultProvider`, `defaultModel`, or API keys.
- **Live config:** `/root/.pi/agent/` (provider `opencode`, model `hy3-free`, literal working keys preserved).
- **Nova layer:** added in prior step; `nova.enabled = true` in `settings.json`.

## 1. Nova block paths — all present in `/root/.pi/agent/nova/`

| Key in `nova` block | Resolved path | Status |
|---|---|---|
| registry | `nova/agent-registry.json` | OK |
| events | `nova/events.json` | OK |
| workflow | `nova/workflow.json` | OK |
| artifactCatalog | `nova/artifact-catalog.json` | OK |
| permissions | `nova/permissions.json` | OK |

## 2. Nova STRUCTURE-ONLY validation — PASSED

A live-specific check (no `models.json`/keys read, no secrets printed) confirmed:
- 15 registered agents, each with full plugin (`agent.json`, `instructions.md`, `tools.json`, `memory.json`, `schemas/`, `validators/`) and input/output contracts.
- 10 workflow phases, each orchestrated and referencing valid agents/events.
- Required lifecycle events present (`PROJECT_CREATED` … `PROJECT_COMPLETED`).
- `artifact-catalog.json`, `permissions.json`, `tool-registry.json` present.

**Conclusion:** the Nova layer itself is structurally sound and consistent on the live system.

## 3. Why `validate_nova.py` fails on live — PRE-EXISTING conflicts, NOT Nova errors

`scripts/validate_nova.py` enforces the shape of the *secured freemodel* configuration. Its failures on the live system are caused by conditions that existed **before** the Nova merge and are **required** by the user's constraints (keep working literal keys; keep current provider). None originate from the Nova layer:

| Validator failure | Root cause | Nova-related? |
|---|---|---|
| `provider freemodel stores a literal API key` / `provider dahl stores a literal API key` | Live `models.json` keeps working literal keys (intentional, step 4 of merge plan) | No |
| `secret-like value found in .pi/agent/models.json` | Same literal keys above | No |
| `default provider/model pair is not present in models.json` | Live `defaultProvider=opencode` but `opencode` is **not listed** in `models.json` providers at all (pre-existing) | No |
| `defaultProvider and modelRouting.defaultProvider differ` | Live `defaultProvider=opencode` vs `modelRouting.defaultProvider=nvidia` (pre-existing mismatch) | No |
| `AOW model claude-fable-5 / sonnet / gemini-3.5-flash is not present in models.json` | AOW models referenced in `settings.json` are absent from `models.json` model lists (pre-existing) | No |

**Proof the conflicts are not Nova defects:** the Nova structural check (section 2) passes; Pi runs successfully against the live config (section 4). The validator's policy checks simply encode a different target configuration than the one intentionally kept live.

## 4. Runtime check — passed

- `settings.json`: valid JSON.
- Fresh new-session Pi run (`pi --print -p "…" --session-dir /tmp/pi-verify-*`) returned the expected reply, exit 0, and created a new session. Pi loads the merged config and calls the model normally.

## 5. Rollback — corrected commands (full filenames)

Backup files (no truncation; earlier display wrapping was cosmetic only):

```
-rw-r--r-- 1 root root    9000  /root/.pi-merge-backup/settings.json.bak-merge-20260821-140118
-rw-r--r-- 1 root root    4251  /root/.pi-merge-backup/models.json.bak-merge-20260821-140118
-rw-r--r-- 1 root root 6372515  /root/.pi.backup-20260821-135129.tar.gz
```

SHA-256:
```
666a0ddf976e93dc50362bed11d6d2b4eeec29f6c4491a4c0295f0efa73d7f97  settings.json.bak-merge-20260821-140118
214485bcf76da42f8dc76601b1725810aa8a7a1655e7f532550853ddb7ffef6a  models.json.bak-merge-20260821-140118
6972c065b61d40483a7a8c402c84ca6c4213d6629cf11e49f514ca3e44466404  pi.backup-20260821-135129.tar.gz
```

### Rollback the Nova merge (restore settings to pre-merge state)
```bash
cp /root/.pi-merge-backup/settings.json.bak-merge-20260821-140118 /root/.pi/agent/settings.json
```
(To also restore keys unchanged: `cp /root/.pi-merge-backup/models.json.bak-merge-20260821-140118 /root/.pi/agent/models.json` — no model change was made, so this is optional.)

### Full rollback to the complete pre-update snapshot
```bash
tar -xzf /root/.pi.backup-20260821-135129.tar.gz -C /root
```

## 6. Out of scope (not done in this verification phase)
- No key rotation, no `defaultProvider`/`defaultModel` change, no `$PI_HOME` switch, no env-ref rewrite. See the final summary for deferred items.

## 7. `nova.enabled` status vs actual orchestration

- **`nova.enabled = true` is active** in `/root/.pi/agent/settings.json` (the config block was added and verified in Step 1).
- **However, actual orchestration execution is NOT yet proven.** The event-driven multi-agent runtime (Orchestrator dispatching the 15 plugins through the 10 phases) requires confirming that **Pi's Runtime actually reads `settings.nova` and acts on it**.
- What was tested: the Nova *files* and *config block* are present and structurally valid, and Pi loads the merged `settings.json` and calls a model normally in a plain session.
- What was NOT tested: that Pi interprets `nova.enabled` to switch into orchestrator mode. Until an independent test proves Pi consumes `settings.nova`, the layer is **config-present but runtime-unverified**.

## 8. Future standalone plan (NOT executed now)

This plan is deferred per the close-out constraints (no key rotation or default-model switch at this time).

### Phase A — Key rotation (security, independent of config)
1. Rotate the `ghp_…` GitHub token exposed in chat (GitHub → Settings → Developer settings → PATs).
2. Rotate the literal `freemodel` (`fe_oa_…`) and `dahl` (`dahl_…`) keys; issue new keys with least privilege.
3. Store new keys **only** in environment variables (`FREEMODEL_API_KEY`, `DAHL_API_KEY`, `NVIDIA_API_KEY`); never in JSON or `.env` committed to the repo.
4. Purge any shell-history / temp copies that captured the old values.

### Phase B — Test `freemodel/gpt-5.4-mini` in this runtime
1. With env vars set, run an isolated test:
   `pi --provider freemodel --model gpt-5.4-mini --print -p "<probe>" --session-dir /tmp/pi-freemodel-test`
2. Confirm the model actually responds in this environment before promoting it to default.

### Phase C — Align configuration ONLY after Phase B passes
1. Set `defaultProvider`/`defaultModel` → `freemodel`/`gpt-5.4-mini`.
2. Align `modelRouting.defaultProvider` to equal `defaultProvider`.
3. Fix AOW model references (`advisorModel`/`workerModel`/`orchestratorModel`) to verified model IDs present in `models.json`.
4. Switch `instructions.files` to `$PI_HOME/…` **only if** Pi is confirmed to expand the variable; otherwise keep literal paths.
5. Replace literal keys in `models.json` with the `$…` env references.

### Phase D — Re-validate
1. Run `scripts/validate_nova.py`; expect a full PASS once keys are env-refs and routing is aligned.

### Phase E — Prove orchestrator runtime
1. Independent test that Pi reads `settings.nova` and drives the event-driven workflow (not just loads the file). Until proven, treat orchestration as unverified.

### Rollback safety throughout
- All steps remain revertible via `/root/.pi-merge-backup/` and `/root/.pi.backup-20260821-135129.tar.gz` (see Section 5).
