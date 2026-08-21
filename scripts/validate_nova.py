#!/usr/bin/env python3
"""Validate the Nova-compatible configuration without contacting external services."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOVA = ROOT / "pi" / "agent" / "nova"
ERRORS: list[str] = []
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"fe_oa_[A-Za-z0-9_-]{10,}"),
    re.compile(r"dahl_[A-Za-z0-9_-]{10,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - validator output path
        ERRORS.append(f"invalid JSON: {path}: {exc}")
        return None


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def main() -> int:
    registry = load(NOVA / "agent-registry.json")
    events = load(NOVA / "events.json")
    workflow = load(NOVA / "workflow.json")
    settings = load(ROOT / "pi" / "agent" / "settings.json")
    models = load(ROOT / "pi" / "agent" / "models.json")

    if not all((registry, events, workflow, settings, models)):
        return report()

    agents = {item["id"]: item for item in registry.get("agents", [])}
    require(len(agents) == 15, f"expected 15 registered agents, found {len(agents)}")
    for agent_id, item in agents.items():
        plugin = ROOT / "pi" / "agent" / "nova" / item["plugin"]
        for required in ("agent.json", "instructions.md", "tools.json", "memory.json", "schemas", "validators"):
            require((plugin / required).exists(), f"missing {required} for plugin {agent_id}")
        require((plugin / item["inputContract"]).exists(), f"missing input contract for {agent_id}")
        require((plugin / item["outputContract"]).exists(), f"missing output contract for {agent_id}")

    event_names = {item["name"] for item in events.get("events", [])}
    required_events = {"PROJECT_CREATED", "REQUIREMENTS_READY", "DESIGN_READY", "CODE_READY", "TEST_FAILED", "FIX_REQUIRED", "DEPLOY_READY", "PROJECT_COMPLETED"}
    require(required_events <= event_names, "event registry is missing one or more required lifecycle events")
    phases = workflow.get("phases", [])
    require(len(phases) == 10, f"expected 10 workflow phases, found {len(phases)}")
    for phase in phases:
        require("orchestrator" in phase.get("agents", []), f"phase {phase.get('id')} is not orchestrated")
        require(set(phase.get("agents", [])) <= set(agents), f"phase {phase.get('id')} references an unknown agent")
        require(phase.get("entryEvent") in event_names, f"phase {phase.get('id')} has unknown entry event")
        require(phase.get("successEvent") in event_names, f"phase {phase.get('id')} has unknown success event")

    provider_models = {
        provider: {model.get("id") for model in data.get("models", [])}
        for provider, data in models.get("providers", {}).items()
    }
    default_provider = settings.get("defaultProvider")
    default_model = settings.get("defaultModel")
    require(default_model in provider_models.get(default_provider, set()), "default provider/model pair is not present in models.json")
    require(default_provider == settings.get("modelRouting", {}).get("defaultProvider"), "defaultProvider and modelRouting.defaultProvider differ")
    for key in ("advisorModel", "workerModel", "orchestratorModel"):
        model_id = settings.get("aow", {}).get(key)
        require(any(model_id in model_ids for model_ids in provider_models.values()), f"AOW model {model_id} is not present in models.json")

    for provider, data in models.get("providers", {}).items():
        api_key = data.get("apiKey")
        require(api_key is None or (isinstance(api_key, str) and api_key.startswith("$")), f"provider {provider} stores a literal API key")

    scan_paths = [ROOT / "pi" / "agent" / "settings.json", ROOT / "pi" / "agent" / "models.json", ROOT / "pi" / "mcp.json", ROOT / "pi" / "agent" / "AGENTS.md"]
    for path in scan_paths:
        text = path.read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            require(not pattern.search(text), f"secret-like value found in {path.relative_to(ROOT)}")

    return report()


def report() -> int:
    if ERRORS:
        print("Nova validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("Nova validation passed: registry, events, workflow, plugins, routing, and secret references are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

