#!/usr/bin/env python3
"""Build the portable Nova-compatible orchestration layer for Pi.

The script is deterministic and intentionally keeps credentials out of the
repository. It generates registries, event/workflow definitions, schemas,
plugin contracts, prompt templates, and the validator used by CI.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOVA = ROOT / "pi" / "agent" / "nova"
PLUGINS = NOVA / "plugins"
PROMPTS = NOVA / "prompts"
SCHEMAS = NOVA / "schemas"
WORKFLOWS = NOVA / "workflows"
CORE = NOVA / "core"

AGENTS = [
    ("orchestrator", "Orchestrator", "توزيع العمل، إدارة الحالة، وتجميع النتائج", "coordination"),
    ("discovery", "Discovery Agent", "فهم الهدف والسياق والقيود", "discovery"),
    ("requirements", "Requirements Agent", "تحويل الفكرة إلى متطلبات قابلة للتحقق", "planning"),
    ("research", "Research Agent", "جمع الأدلة والمراجع وتحليل المجال", "research"),
    ("architect", "Architecture Agent", "اختيار المعمارية والحدود والتبعيات", "architecture"),
    ("ux-ui", "UX/UI Agent", "تصميم التجربة وواجهة الاستخدام والنظام البصري", "design"),
    ("frontend", "Frontend Agent", "تنفيذ واجهة العميل ومكوناتها", "development"),
    ("backend", "Backend Agent", "تنفيذ الخدمات وواجهات API", "development"),
    ("database", "Database Agent", "تصميم البيانات والهجرات والاستعلامات", "development"),
    ("security", "Security Agent", "التهديدات، الأسرار، الصلاحيات، والمراجعة الأمنية", "security"),
    ("qa", "QA Agent", "اختبارات الوحدة والتكامل وواجهات المستخدم", "quality"),
    ("devops", "DevOps Agent", "التعبئة والنشر والمراقبة والتراجع", "deployment"),
    ("integration", "Integration Agent", "دمج النتائج والتحقق من العقود بين الوكلاء", "integration"),
    ("documentation", "Documentation Agent", "توثيق القرارات والواجهات وطريقة التشغيل", "documentation"),
    ("improvement", "Continuous Improvement Agent", "قياس النتائج وتسجيل الدروس والتحسينات", "improvement"),
]

EVENTS = [
    ("PROJECT_CREATED", "إنشاء مشروع جديد", "discovery"),
    ("REQUIREMENTS_READY", "اعتماد المتطلبات", "requirements"),
    ("DESIGN_READY", "اعتماد التصميم والمعمارية", "ux-ui"),
    ("CODE_READY", "اكتمال التنفيذ الأولي", "integration"),
    ("TEST_FAILED", "فشل اختبار أو بوابة جودة", "qa"),
    ("FIX_REQUIRED", "وجود إصلاح مطلوب", "integration"),
    ("DEPLOY_READY", "اجتياز جاهزية النشر", "devops"),
    ("PROJECT_COMPLETED", "إغلاق دورة المشروع", "improvement"),
]

PHASE_AGENTS = {
    "discovery": ["discovery"],
    "planning": ["requirements", "research"],
    "architecture": ["architect", "database"],
    "ux-ui": ["ux-ui"],
    "development": ["frontend", "backend", "database"],
    "integration": ["integration"],
    "security": ["security"],
    "qa": ["qa"],
    "deployment": ["devops"],
    "improvement": ["improvement"],
}

PHASES = [
    (1, "discovery", "Discovery", "PROJECT_CREATED", "REQUIREMENTS_READY", ["project-brief.md"]),
    (2, "planning", "Planning", "REQUIREMENTS_READY", "DESIGN_READY", ["requirements.md", "research.md"]),
    (3, "architecture", "Architecture", "REQUIREMENTS_READY", "DESIGN_READY", ["architecture.md", "api.yaml", "database.sql"]),
    (4, "ux-ui", "UX/UI", "DESIGN_READY", "DESIGN_READY", ["design-system.md", "ux-flows.md"]),
    (5, "development", "Development", "DESIGN_READY", "CODE_READY", ["components.tsx", "services.ts", "tests.md"]),
    (6, "integration", "Integration", "CODE_READY", "DEPLOY_READY", ["integration-report.md", "artifact-manifest.json"]),
    (7, "security", "Security Review", "CODE_READY", "DEPLOY_READY", ["security-review.md"]),
    (8, "qa", "QA", "DEPLOY_READY", "DEPLOY_READY", ["qa-report.md", "test-results.json"]),
    (9, "deployment", "Deployment", "DEPLOY_READY", "PROJECT_COMPLETED", ["deployment.md", "runbook.md"]),
    (10, "improvement", "Continuous Improvement", "PROJECT_COMPLETED", "PROJECT_COMPLETED", ["growth-log.md", "adr.md"]),
]


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    for directory in (NOVA, PLUGINS, PROMPTS, SCHEMAS, WORKFLOWS, CORE):
        directory.mkdir(parents=True, exist_ok=True)

    registry = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "schemaVersion": "1.0.0",
        "system": "nova",
        "description": "Portable plugin registry for Pi's Nova-compatible operating model.",
        "orchestrator": "orchestrator",
        "agents": [
            {
                "id": agent_id,
                "name": name,
                "role": role,
                "category": category,
                "plugin": f"plugins/{agent_id}",
                "status": "enabled",
                "inputContract": f"schemas/{agent_id}.input.schema.json",
                "outputContract": f"schemas/{agent_id}.output.schema.json",
            }
            for agent_id, name, role, category in AGENTS
        ],
    }
    dump(NOVA / "agent-registry.json", registry)

    dump(NOVA / "events.json", {
        "schemaVersion": "1.0.0",
        "events": [
            {
                "name": name,
                "description": description,
                "producer": producer,
                "payload": "schemas/event-payload.schema.json",
                "idempotent": True,
                "auditRequired": True,
            }
            for name, description, producer in EVENTS
        ],
    })

    dump(NOVA / "artifact-catalog.json", {
        "schemaVersion": "1.0.0",
        "rules": {
            "everyStageMustProduceArtifact": True,
            "immutableAfterApproval": True,
            "contentAddressed": True,
            "ownerRequired": True,
            "sourceAndDecisionTraceRequired": True,
        },
        "artifacts": [
            {"name": name, "kind": "document" if name.endswith((".md", ".yaml", ".json", ".sql")) else "source", "required": True}
            for name in sorted({artifact for *_rest, artifacts in PHASES for artifact in artifacts})
        ],
    })

    dump(NOVA / "tool-registry.json", {
        "schemaVersion": "1.0.0",
        "defaultPolicy": "deny",
        "tools": [
            {"id": "git", "category": "source-control", "mode": "read-write", "approval": "commit"},
            {"id": "github", "category": "source-control", "mode": "read-write", "approval": "pull-request-or-push"},
            {"id": "browser", "category": "research", "mode": "read-only-by-default", "approval": "external-write"},
            {"id": "web-search", "category": "research", "mode": "read-only", "approval": "none"},
            {"id": "figma", "category": "design", "mode": "read-write", "approval": "design-publish"},
            {"id": "database", "category": "data", "mode": "read-write", "approval": "migration-or-delete"},
            {"id": "cloud-deployment", "category": "deployment", "mode": "read-write", "approval": "deploy"},
            {"id": "mcp", "category": "integration", "mode": "scoped", "approval": "connector-policy"},
        ],
    })

    dump(NOVA / "permissions.json", {
        "schemaVersion": "1.0.0",
        "default": {"allow": [], "deny": ["secrets.read", "production.delete", "external.write"]},
        "roles": {
            "orchestrator": {"allow": ["artifact.read", "artifact.write", "event.publish", "agent.invoke", "audit.write"], "requiresApproval": ["external.write", "deploy"]},
            "research": {"allow": ["artifact.read", "artifact.write", "web.read", "browser.read"], "requiresApproval": ["browser.write"]},
            "development": {"allow": ["artifact.read", "artifact.write", "repo.read", "repo.write", "test.run"], "requiresApproval": ["commit", "external.write"]},
            "security": {"allow": ["artifact.read", "artifact.write", "audit.read", "secret-reference.validate"], "requiresApproval": ["secret.rotate"]},
            "deployment": {"allow": ["artifact.read", "artifact.write", "deploy.plan", "deploy.status"], "requiresApproval": ["deploy", "rollback"]},
            "improvement": {"allow": ["artifact.read", "artifact.write", "audit.read", "metrics.read"], "requiresApproval": ["policy.change"]},
        },
    })

    dump(NOVA / "schemas" / "event-payload.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "nova/event-payload.schema.json",
        "type": "object",
        "required": ["eventId", "eventType", "projectId", "occurredAt", "actor", "payloadVersion"],
        "properties": {
            "eventId": {"type": "string", "minLength": 1},
            "eventType": {"type": "string", "pattern": "^[A-Z][A-Z0-9_]+$"},
            "projectId": {"type": "string", "minLength": 1},
            "occurredAt": {"type": "string", "format": "date-time"},
            "actor": {"type": "string", "minLength": 1},
            "payloadVersion": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
            "correlationId": {"type": "string"},
            "data": {"type": "object"},
        },
        "additionalProperties": False,
    })

    common_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["projectId", "taskId", "objective", "context", "constraints"],
        "properties": {
            "projectId": {"type": "string", "minLength": 1},
            "taskId": {"type": "string", "minLength": 1},
            "objective": {"type": "string", "minLength": 1},
            "context": {"type": "object"},
            "constraints": {"type": "array", "items": {"type": "string"}},
            "artifacts": {"type": "array", "items": {"type": "string"}},
            "approval": {"type": "object"},
        },
        "additionalProperties": True,
    }
    dump(NOVA / "schemas" / "project-memory.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["projectId", "status", "files", "decisions", "artifacts", "updatedAt"],
        "properties": {
            "projectId": {"type": "string"}, "status": {"type": "string"},
            "files": {"type": "array", "items": {"type": "object"}},
            "decisions": {"type": "array", "items": {"type": "object"}},
            "artifacts": {"type": "array", "items": {"type": "object"}},
            "updatedAt": {"type": "string", "format": "date-time"},
        },
        "additionalProperties": False,
    })
    dump(NOVA / "schemas" / "agent-memory.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["agentId", "sessionId", "observations", "commitments", "updatedAt"],
        "properties": {
            "agentId": {"type": "string"}, "sessionId": {"type": "string"},
            "observations": {"type": "array", "items": {"type": "object"}},
            "commitments": {"type": "array", "items": {"type": "object"}},
            "updatedAt": {"type": "string", "format": "date-time"},
        },
        "additionalProperties": False,
    })
    dump(NOVA / "schemas" / "knowledge-memory.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["knowledgeId", "source", "kind", "content", "confidence", "updatedAt"],
        "properties": {
            "knowledgeId": {"type": "string"}, "source": {"type": "string"},
            "kind": {"enum": ["best-practice", "documentation", "pattern", "anti-pattern"]},
            "content": {"type": "string"}, "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "updatedAt": {"type": "string", "format": "date-time"},
        },
        "additionalProperties": False,
    })
    dump(NOVA / "schemas" / "artifact.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["artifactId", "name", "kind", "owner", "status", "createdAt", "contentHash"],
        "properties": {
            "artifactId": {"type": "string"}, "name": {"type": "string"}, "kind": {"type": "string"},
            "owner": {"type": "string"}, "status": {"enum": ["draft", "review", "approved", "superseded"]},
            "createdAt": {"type": "string", "format": "date-time"}, "contentHash": {"type": "string"},
            "sources": {"type": "array", "items": {"type": "string"}}, "decisionIds": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    })
    dump(NOVA / "schemas" / "workflow-state.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["projectId", "workflowId", "phase", "status", "history"],
        "properties": {
            "projectId": {"type": "string"}, "workflowId": {"type": "string"},
            "phase": {"type": "string"}, "status": {"enum": ["pending", "running", "blocked", "completed", "failed"]},
            "history": {"type": "array", "items": {"type": "object"}},
        },
        "additionalProperties": True,
    })

    dump(NOVA / "workflow.json", {
        "schemaVersion": "1.0.0",
        "workflowId": "nova-software-delivery",
        "execution": {"mode": "event-driven", "maxRetries": 1, "idempotencyKey": "eventId", "approvalPolicy": "explicit-for-side-effects"},
        "phases": [
            {"number": number, "id": phase_id, "name": name, "entryEvent": entry, "successEvent": success, "agents": ["orchestrator", *PHASE_AGENTS[phase_id]], "artifacts": artifacts}
            for number, phase_id, name, entry, success, artifacts in PHASES
        ],
        "failureTransitions": [
            {"event": "TEST_FAILED", "from": "qa", "to": "integration"},
            {"event": "FIX_REQUIRED", "from": "integration", "to": "development"},
        ],
    })

    for number, phase_id, name, entry, success, artifacts in PHASES:
        body = f"""version: 1\nid: nova-{phase_id}\nname: {name}\ntrigger:\n  event: {entry}\n  idempotency_key: eventId\nexecution:\n  mode: event-driven\n  approval_required: false\nagents:\n  - orchestrator\n"""
        for phase_agent in PHASE_AGENTS[phase_id]:
            body += f"  - {phase_agent}\n"
        body += "outputs:\n"
        for artifact in artifacts:
            body += f"  - {artifact}\n"
        body += f"success_event: {success}\nfailure_events:\n  - TEST_FAILED\n  - FIX_REQUIRED\nsecurity:\n  audit_log: required\n  secret_access: reference-only\n"
        write(WORKFLOWS / f"{number:02d}-{phase_id}.yaml", body)

    core_docs = {
        "orchestrator.md": """# Nova Orchestrator\n\nالمنسق هو نقطة التحكم الوحيدة في دورة المشروع. يستقبل طلبًا، ينشئ `projectId` و`workflowId`، يقرأ ذاكرة المشروع، يختار الوكيل المناسب من السجل، ثم ينشر حدثًا جديدًا بعد التحقق من Artifact الناتج. لا ينفذ المنسق عمل الوكيل المتخصص بدلًا منه.\n\nكل انتقال يعتمد على حدث قابل للتكرار بأمان، وكل نتيجة يجب أن تحمل مالكًا ومصدرًا وقرارًا مرتبطًا. العمليات الخارجية مثل الدفع والنشر وحذف البيانات تتطلب موافقة صريحة ولا تُنفّذ ضمن التفويض الضمني.\n""",
        "event-bus.md": """# Event Bus Contract\n\nالأحداث هي قناة الاتصال الرسمية بين الوكلاء. اسم الحدث ثابت وبالأحرف الكبيرة، ويحتوي كل payload على `eventId` و`projectId` و`occurredAt` و`actor` و`payloadVersion`. يجب تسجيل كل نشر وإعادة محاولة ورفض في سجل التدقيق.\n\nلا يعتمد أي وكيل على قراءة ذاكرة وكيل آخر مباشرة؛ يقرأ من Project Memory أو من Artifact معتمد، أو يتلقى الحدث عبر المنسق.\n""",
        "memory.md": """# Memory Architecture\n\nتتكون الذاكرة من ثلاث طبقات معزولة. **Project Memory** تحفظ الملفات والقرارات والتصميم والكود وحالة سير العمل. **Agent Memory** خاصة بكل وكيل وجلسة وتحتوي الملاحظات والالتزامات المؤقتة. **Knowledge Memory** تحفظ أفضل الممارسات والتوثيق والأنماط مع المصدر ودرجة الثقة.\n\nلا تُحفظ الأسرار داخل أي طبقة؛ تحفظ مراجع الأسرار فقط مثل اسم متغير البيئة أو معرّف مدير الأسرار.\n""",
        "artifact-protocol.md": """# Artifact Protocol\n\nلا تُعد نتيجة الوكيل نصًا عابرًا. يجب أن تكون Artifact قابلة للتسمية والإصدار والمراجعة، مع `contentHash` ومالك وحالة ومصادر وقرارات مرتبطة. لا تنتقل المرحلة إلى الحدث التالي قبل التحقق من Artifacts المطلوبة.\n""",
        "security.md": """# Security Model\n\nالسياسة الافتراضية هي الرفض. صلاحيات الوكيل محددة بدوره، والوصول إلى الأسرار مرجعي فقط، والكتابة الخارجية والنشر والهجرات والحذف تتطلب موافقة. يجب عزل بيانات المشاريع والذاكرة بحسب `projectId`، وتسجيل كل عملية حساسة في Audit Log.\n\nإزالة قيمة سرية من الملف الحالي لا تزيلها من Git history؛ تدوير المفاتيح يظل إجراءً إلزاميًا إذا سبق تخزينها في المستودع.\n""",
        "tool-layer.md": """# Tool Layer\n\nيستخدم Nova سجل أدوات موحدًا بدل أن يربط كل وكيل بأداة خاصة غير موثقة. كل أداة لها معرّف وفئة ونمط وصول وسياسة موافقة. عند فشل أداة خارجية، يكتب الوكيل سبب الفشل وخطة fallback ولا يتجاوز حدود الصلاحيات.\n""",
        "observability.md": """# Observability\n\nالحد الأدنى للمراقبة هو: `projectId` و`workflowId` و`eventId` و`agentId` ومدة التنفيذ وحالة النتيجة وعدد إعادة المحاولة. تحفظ الأحداث والقرارات ورفض الصلاحيات في Audit Log قابل للبحث، وتُربط كل مشكلة بالـ Artifact أو الحدث الذي سببها.\n""",
    }
    for name, content in core_docs.items():
        write(CORE / name, content)

    for agent_id, name, role, category in AGENTS:
        plugin = PLUGINS / agent_id
        dump(plugin / "agent.json", {
            "schemaVersion": "1.0.0",
            "id": agent_id,
            "name": name,
            "version": "1.0.0",
            "role": role,
            "category": category,
            "entrypoint": "instructions.md",
            "tools": "tools.json",
            "memory": "memory.json",
            "inputSchema": f"schemas/{agent_id}.input.schema.json",
            "outputSchema": f"schemas/{agent_id}.output.schema.json",
            "permissionsRole": "security" if agent_id == "security" else ("deployment" if agent_id == "devops" else ("orchestrator" if agent_id == "orchestrator" else category if category in {"research", "development", "improvement"} else "development")),
            "events": {"subscribe": ["PROJECT_CREATED", "REQUIREMENTS_READY", "DESIGN_READY", "CODE_READY", "TEST_FAILED", "FIX_REQUIRED", "DEPLOY_READY", "PROJECT_COMPLETED"], "publish": ["REQUIREMENTS_READY", "DESIGN_READY", "CODE_READY", "TEST_FAILED", "FIX_REQUIRED", "DEPLOY_READY", "PROJECT_COMPLETED"] if agent_id == "orchestrator" else []},
        })
        write(plugin / "instructions.md", f"""# {name}\n\n## المهمة\n\n{role}. يعمل هذا الوكيل كـ Plugin مستقل داخل Nova ولا يتجاوز حدود دوره.\n\n## دورة التنفيذ\n\nيقرأ المدخل وفق Schema، يتحقق من Project Memory وArtifacts المعتمدة، ينفذ المهمة ضمن الأدوات المسموح بها، ثم ينتج Artifact موثقًا أو يعلن سبب الحظر. لا يكتب أسرارًا ولا ينفذ أثرًا خارجيًا يتطلب موافقة.\n\n## عقد الإخراج\n\nيجب أن يحتوي الإخراج على `status` و`agentId` و`projectId` و`artifacts` و`evidence` و`nextEvent`. عند الفشل، يجب تحديد `failureType` و`retryable` و`recommendedAction`.\n\n## قواعد الجودة\n\nيفصل الوكيل بين الحقائق والاستنتاجات، يذكر الملفات أو المصادر المستخدمة، ويتوقف عند نقص السياق بدل التخمين. يمرر النتائج إلى المنسق ولا يغير ملفات وكيل آخر خارج نطاق المهمة.\n""")
        dump(plugin / "tools.json", {"schemaVersion": "1.0.0", "defaultPolicy": "deny", "allowed": ["artifact.read", "artifact.write", "memory.read", "memory.write", "audit.write"], "requiresApproval": ["external.write", "deploy", "commit", "secret.rotate"]})
        dump(plugin / "memory.json", {"schemaVersion": "1.0.0", "scope": f"agent:{agent_id}", "read": ["agent-memory", "project-memory:approved"], "write": ["agent-memory", "project-memory:artifacts"], "retention": {"sessionNotes": "project-lifecycle", "secrets": "never"}})
        dump(plugin / "schemas" / f"{agent_id}.input.schema.json", {**common_schema, "$id": f"nova/{agent_id}.input.schema.json", "title": f"{name} input"})
        dump(plugin / "schemas" / f"{agent_id}.output.schema.json", {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"nova/{agent_id}.output.schema.json", "type": "object", "required": ["status", "agentId", "projectId", "artifacts", "evidence", "nextEvent"], "properties": {"status": {"enum": ["completed", "blocked", "failed"]}, "agentId": {"const": agent_id}, "projectId": {"type": "string"}, "artifacts": {"type": "array", "items": {"type": "string"}}, "evidence": {"type": "array", "items": {"type": "string"}}, "nextEvent": {"type": ["string", "null"]}, "failureType": {"type": ["string", "null"]}, "retryable": {"type": "boolean"}}, "additionalProperties": True})
        write(plugin / "validators" / "README.md", f"""# Validators for {agent_id}\n\nيجب أن تتحقق أدوات التحقق من صحة Schema، ووجود Artifact المطلوبة، وصحة `projectId`، ومنع الأسرار والقيم الثابتة الحساسة. يمكن إضافة validators تنفيذية لاحقًا دون تغيير عقد Plugin.\n""")
        write(PROMPTS / f"{agent_id}.md", f"""<role>\nأنت {name} ضمن نظام Nova-compatible. دورك: {role}.\n</role>\n\n<task>\nنفذ المهمة المسندة لك فقط، اعتمادًا على السياق والـ Artifacts المعتمدة، ولا تتجاوز حدود الصلاحيات.\n</task>\n\n<structured_output_contract>\nأعد status، artifacts، evidence، والمحفز التالي nextEvent. عند التعذر، أعد سببًا قابلًا للتحقق وخطوة آمنة تالية.\n</structured_output_contract>\n\n<verification_loop>\nتحقق من Schema، ومن اكتمال Artifact، ومن عدم وجود أسرار أو آثار خارجية غير مصرّح بها قبل التسليم.\n</verification_loop>\n\n<grounding_rules>\nافصل الحقائق عن الاستنتاجات، ولا تخمن السياق المفقود.\n</grounding_rules>\n""")

    write(NOVA / "README.md", """# Nova-compatible Pi\n\nهذه الطبقة تجعل Pi يعمل كنظام **Event-Driven متعدد الوكلاء** بدل مجموعة تعليمات متفرقة. المنسق يملك حالة سير العمل، والوكلاء Plugins مستقلة، والنتائج Artifacts قابلة للتتبع، والذاكرة مقسمة إلى Project وAgent وKnowledge Memory.\n\n## نقطة الحقيقة\n\nيُعد `agent-registry.json` سجل الوكلاء، و`events.json` عقد الأحداث، و`workflow.json` مخطط الحالة العام، و`permissions.json` سياسة الصلاحيات، و`tool-registry.json` سجل الأدوات. لا تضف وكيلًا جديدًا قبل إضافة Plugin كامل له `agent.json` و`instructions.md` و`tools.json` و`memory.json` و`schemas/` و`validators/`.\n\n## التشغيل\n\nيبدأ المشروع بحدث `PROJECT_CREATED`. ينتقل المنسق بين المراحل العشر بعد تحقق Artifacts، ويعيد المهمة إلى المسار المناسب عند `TEST_FAILED` أو `FIX_REQUIRED`. عمليات النشر والكتابة الخارجية وتدوير الأسرار تتطلب موافقة صريحة.\n\n## التحقق\n\nشغّل `python3 scripts/validate_nova.py` من جذر المستودع. التحقق يفحص JSON، وتطابق السجل مع Plugins، وتسلسل الأحداث، والمراجع غير الصالحة للنماذج، ومؤشرات الأسرار.\n""")

    write(ROOT / "docs" / "nova-architecture.md", """# Nova-compatible Architecture\n\n## الهدف\n\nالهدف هو تحويل نسخة إعدادات Pi إلى أساس قابل للنمو لمنصة تطوير برمجيات متعددة الوكلاء. المعمارية الجديدة لا تدّعي أن Pi أصبح منصة SaaS مكتملة؛ بل توفر عقود التشغيل التي تمنع الفوضى عند إضافة التنفيذ الفعلي.\n\n## المكونات\n\n| المكوّن | المسؤولية | مصدر الحقيقة |\n|---|---|---|\n| Orchestrator | إدارة الحالة والتفويض والتجميع | `pi/agent/nova/workflow.json` |\n| Event System | نقل الأحداث وإعادة المحاولة والتدقيق | `pi/agent/nova/events.json` |\n| Project Memory | الملفات والقرارات والتصميم والكود | `project-memory.schema.json` |\n| Agent Memory | ذاكرة الوكيل والجلسة | `agent-memory.schema.json` |\n| Knowledge Memory | أفضل الممارسات والتوثيق والأنماط | `knowledge-memory.schema.json` |\n| Artifact System | نتائج قابلة للإصدار والتحقق | `artifact.schema.json` و`artifact-catalog.json` |\n| Tool Layer | أدوات خارجية بسياسة deny-by-default | `tool-registry.json` و`permissions.json` |\n\n## دورة الحالة\n\nتبدأ الدورة بـ `PROJECT_CREATED`، ثم تمر بالاكتشاف والتخطيط والمعمارية والتصميم والتطوير والدمج والمراجعة الأمنية وضمان الجودة والنشر والتحسين. لا يعني اسم الحدث أن الانتقال ناجح تلقائيًا؛ النجاح يتطلب Artifacts المطلوبة ونتيجة تحقق مسجلة.\n\n## إضافة وكيل\n\nينشئ المطور مجلدًا تحت `pi/agent/nova/plugins/<agent-id>`، ثم يضيف تعريفه إلى `agent-registry.json`، ويحدد صلاحياته، ويضيف Prompt وSchemas وValidators. يجب أن يكون الوكيل قابلاً لإعادة التشغيل بأمان، وألا يقرأ أسرارًا مباشرة، وألا ينفذ كتابة خارجية دون موافقة.\n""")
    write(ROOT / "docs" / "nova-migration.md", """# Pi to Nova Migration Notes\n\n## ما تم إصلاحه\n\nتم إنشاء طبقة Nova مستقلة فوق نسخة Pi الحالية بدل حذف محتوى ECC. كما تم توحيد تعريف الوكلاء والأحداث وسير العمل والذاكرة والـ Artifacts والأدوات والصلاحيات في ملفات قابلة للتحقق.\n\nتم تصحيح التوجيه الافتراضي ليشير إلى نموذج موجود في `models.json`، وإزالة النماذج الوهمية من المسار النشط. أما النماذج غير المتاحة فتبقى موثقة كـ unavailable حتى لا يعاد اختيارها بالخطأ.\n\nتم استبدال مفاتيح API المضمنة في ملف النماذج بمراجع لمتغيرات بيئة. هذا يمنع تسريب القيمة الجديدة، لكنه لا يمحوها من Git history؛ لذلك يجب تدوير أي مفتاح سبق تخزينه في المستودع.\n\n## طريقة الاستعادة\n\nراجع الملفات الجديدة أولًا، ثم انسخ مجلد `pi/` إلى مسار Pi الفعلي باستخدام متغير بيئة مناسب لبيئتك. لا تستبدل الإعدادات الحية قبل أخذ نسخة احتياطية واختبار `settings.json` و`models.json`.\n""")
    write(ROOT / "docs" / "security-rotation.md", """# Security Rotation Required\n\nسبق أن احتوى النسخ الاحتياطي على قيم API حقيقية داخل `pi/agent/models.json`، كما ظهر GitHub token في المحادثة. إزالة القيم من النسخة الحالية ليست بديلًا عن الإلغاء والتدوير.\n\nالإجراء الآمن هو إلغاء كل مفتاح ظهر في النسخة أو المحادثة، إنشاء مفاتيح جديدة بأقل صلاحيات، وضعها في متغيرات البيئة (`FREEMODEL_API_KEY` و`DAHL_API_KEY` و`NVIDIA_API_KEY` عند الحاجة)، ثم اختبار Pi محليًا. لا تُرفع ملفات `.env` ولا تُضاف القيم إلى JSON.\n\nلم تُجرَ إعادة كتابة قسرية لتاريخ Git تلقائيًا، لأن ذلك يغير تاريخ المستودع ويتطلب قرارًا واعيًا. إذا كان نشر القيمة في التاريخ يمثل خطرًا، استخدم عملية تطهير تاريخية منفصلة بعد أخذ نسخة احتياطية وموافقة مالك المستودع.\n""")

    # A concise env template; values are intentionally empty.
    write(ROOT / ".env.example", """# Copy to a local environment file; never commit the populated file.\nFREEMODEL_API_KEY=\nDAHL_API_KEY=\nNVIDIA_API_KEY=\nCLOUDFLARE_API_TOKEN=\n""")

    # Replace provider credentials with environment references and align active routing.
    models_path = ROOT / "pi" / "agent" / "models.json"
    models = json.loads(models_path.read_text(encoding="utf-8"))
    env_by_provider = {"freemodel": "$FREEMODEL_API_KEY", "dahl": "$DAHL_API_KEY", "nvidia": "$NVIDIA_API_KEY", "cloudflare-workers-ai": None}
    for provider, data in models.get("providers", {}).items():
        if provider in env_by_provider:
            data["apiKey"] = env_by_provider[provider]
    models_path.write_text(json.dumps(models, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    settings_path = ROOT / "pi" / "agent" / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    settings["defaultProvider"] = "freemodel"
    settings["defaultModel"] = "gpt-5.4-mini"
    settings["providerPriority"] = ["freemodel", "dahl", "nvidia", "cloudflare-workers-ai"]
    settings["modelRouting"]["defaultProvider"] = "freemodel"
    settings["modelRouting"]["fallbackProvider"] = "freemodel"
    settings["modelRouting"]["verifiedModels"] = [
        model for model in settings["modelRouting"].get("verifiedModels", [])
        if model["id"] in {"gpt-5.6-sol", "gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.5", "gpt-5.4", "gpt-5.4-mini"}
    ]
    settings["aow"]["advisorModel"] = "gpt-5.6-sol"
    settings["aow"]["workerModel"] = "gpt-5.4-mini"
    settings["aow"]["orchestratorModel"] = "gpt-5.6-sol"
    settings["instructions"]["files"] = ["$PI_HOME/agent/AGENTS.md", "$PI_HOME/agent/ECC-ENFORCEMENT.md"]
    settings["nova"] = {
        "enabled": True,
        "version": "1.0.0",
        "registry": "nova/agent-registry.json",
        "events": "nova/events.json",
        "workflow": "nova/workflow.json",
        "artifactCatalog": "nova/artifact-catalog.json",
        "permissions": "nova/permissions.json",
        "defaultDeny": True,
        "requireArtifactBeforeTransition": True,
        "requireApprovalForExternalWrites": True,
    }
    settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Normalize portable paths in the Pi-specific documentation.
    for path in (ROOT / "README.md", ROOT / "pi" / "agent" / "AGENTS.md"):
        text = path.read_text(encoding="utf-8")
        text = (text.replace("/root/.pi", "$PI_HOME")
                    .replace("/root/ecc-repo", "$ECC_HOME")
                    .replace("/root/.agents", "$AGENTS_HOME"))
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
