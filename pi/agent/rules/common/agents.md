# Agent Orchestration

## Available Agents

Located in `~/.pi/agent/agents/`:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| planner | Implementation planning | Complex features, refactoring |
| architect | System design | Architectural decisions |
| tdd-guide | Test-driven development | New features, bug fixes |
| code-reviewer | Code review | After writing code |
| security-reviewer | Security analysis | Before commits |
| build-error-resolver | Fix build errors | When build fails |
| e2e-runner | E2E testing | Critical user flows |
| refactor-cleaner | Dead code cleanup | Code maintenance |
| doc-updater | Documentation | Updating docs |

## Immediate Agent Usage

**لا تحتاج لطلب المستخدم:**
1. طلب ميزات معقدة - استخدم **planner** agent
2. كتابة/تعديل كود - استخدم **code-reviewer** agent
3. إصلاح خلل / ميزة جديدة - استخدم **tdd-guide** agent
4. قرار معماري - استخدم **architect** agent

## Parallel Task Execution

**استخدم دائماً التنفيذ المتوازي للمهام المستقلة:**

```markdown
# GOOD: Parallel execution
تشغيل 3 وكلاء بالتوازي:
1. الوكيل 1: تحليل أمني لوحدة المصادقة
2. الوكيل 2: مراجعة أداء نظام الكاش
3. الوكيل 3: التحقق من الأنواع في الأدوات

# BAD: Sequential when unnecessary
أولاً الوكيل 1، ثم الوكيل 2، ثم الوكيل 3
```

## Delegation Completion Contract

**ينطبق على كل وكيل في كل مستوى (أب، اب، حفيد):**

1. **رسالتك الأخيرة هي المخرجات.** لا تنهي دورك بـ "أنتظر الوكلاء المbackground" - المهمة المُ delegated ليست مهمة مكتملة. إنهاء دورك بينما الأبناء يعملون يفقد نتائجهم.

2. **إذا أ delegatedت، فأنت تملك الجمع.** انتظر النتائج، ادمجها، ثم أرجع. الإ delegated بدون تجميع محظور.

3. **افصل فقط عندما لا يمكن العمل في سياق واحد.** لا تعيد delegation لمهمة مقاسة بالفعل لوكيل واحد - العمق نتيجة، وليس خطة.

> **التبرير:** وضع فشل مُراقب - وكلاء البحث تبعوا "Parallel Task Execution" أعلاه، أطلقوا أبناء، وعادوا بـ "أنتظر" كإجابة نهائية. جميع الأبناء أكتملوا بنجاح لكن نتائجهم فقدت.

## Multi-Perspective Analysis

**للمشاكل المعقدة، استخدم وكلاء الأدوار المقسمة:**
- مراجع حقائق
- مهندس أول
- خبير أمن
- مراجع اتساق
- فاحص تكرار

## When to Use Which Agent

```
طلب ميزة معقدة     → planner
كتب/عدّل كود       → code-reviewer
إصلاح خلل / ميزة جديدة → tdd-guide
قرار معماري         → architect
كود حساس أمنياً     → security-reviewer
فشل بناء            → build-error-resolver
تدفقات مستخدم حرجة → e2e-runner
تنظيف كود ميت      → refactor-cleaner
تحديث وثائق       → doc-updater
```
