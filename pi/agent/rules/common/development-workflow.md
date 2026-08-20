# Development Workflow

> This file extends [common/git-workflow.md](./git-workflow.md) with the full feature development process that happens before git operations.

The Feature Implementation Workflow describes the development pipeline: research, planning, TDD, code review, and then committing to git.

## Feature Implementation Workflow (الموسع)

### المرحلة 0: البحث وإعادة الاستخدام _(إلزامي)_

   - **GitHub code search first:** Run `gh search repos` and `gh search code` to find existing implementations
   - **Library docs second:** Use Context7 or primary vendor docs
   - **Exa only when insufficient:** Use Exa for broader web research
   - **Check package registries:** npm, PyPI, crates.io قبل كتابة كود جديد
   - **Search for adaptable implementations:** حلول موجودة تغطي 80%+

### المرحلة 1: التخطيط
   - استخدم **planner** agent
   - أنشئ: PRD، architecture، system_design، tech_doc، task_list
   - حدد التبعيات والمخاطر
   - **قدّر حجم العمل**: هل يحتاج سوَرْم؟

### المرحلة 2: إدارة السياق _(جديد)_
   - **قبل البدء**: تأكد من وجود سياق كافٍ
   - إذا < 30% متبقي → /compact أولاً
   - إذا المهمة كبيرة → فكر في بدء جلسة جديدة
   - لا تبدأ مهمة جديدة والسياق منخفض

### المرحلة 3: TDD
   - استخدم **tdd-guide** agent
   - RED → GREEN → REFACTOR
   - تحقق من تغطية 80%+
   - اكتب: Unit + Integration + E2E حسب الحاجة

### المرحلة 4: السوَرْم (للمهام المعقدة) _(جديد)_
   - **إذا المهمة تحتوي 3+ طبقات مستقلة**:
     - استخدم نمط المنسق-عمال (Coordinator-Workers)
     - وزّع: Backend، Frontend، DB، Tests
     - اشتغل بالتوازي في branches منفصلة
     - اختبر كل وحدة قبل الدمج
   - **إذا المهمة بسيطة**: تجاوز هذه المرحلة

### المرحلة 5: مراجعة الكود
   - استخدم **code-reviewer** agent فوراً
   - address CRITICAL و HIGH
   - fix MEDIUM إن أمكن
   - للمهام المسوَّرمة: راجع كل PR من Workers

### المرحلة 6: الأمان
   - استخدم **security-reviewer** agent
   - تحقق من: hardcoded keys، injection، auth
   - لا تcommit أبداً بدون مراجعة أمنية

### المرحلة 7: التثبيت والدفع
   - Conventional Commits
   - رسائل commit مفصلة
   - راجع [git-workflow.md](./git-workflow.md)

### المرحلة 8: التعلم _(جديد)_
   - استخرج instincts من الجلسة (Continuous Learning)
   - سجّل Growth Log إذا كان هناك درس
   - وثّق ADRs للقرارات المعمارية
   - هل هناك pattern يتكرر؟ استخرجه

### المرحلة 9: التقييم الذاتي بـ 4 مستويات _(جديد)_
   - **T1 - Structural**: هل اتبعت القواعد؟ (تخطيط، TDD، جودة)
   - **T2 - Security**: هل هناك ثغرات أمنية؟
   - **T3 - Trigger**: هل النموذج والمهارة مناسبان؟
   - **T4 - Behavioral**: هل حللت المشكلة فعلاً؟
   - قبل التسليم: T1+T2
   - بعد المهمة المعقدة: T1+T2+T3
   - نهاية الجلسة: T4 + Growth Log

### المرحلة 10: التطوير الذاتي _(جديد)_
   - هل لاحظت بطء أو تكرار؟ خطط للتحسين
   - هل يمكن إضافة rule جديد؟
   - هل يمكن تحسين skill موجود؟
   - هل التعليمات الحالية واضحة؟

---

## 📐 قواعد بناء البرومبتات (مستوحاة من Codex Plugin)

### الهيكل الأساسي

بالنسبة للمهام المعقدة (تشخيص، إصلاح، مراجعة، بحث)، استخدم XML tags:

```xml
<task>
المهمة بالضبط - ماذا، أين، إلى متى
</task>

<structured_output_contract>
// استخدم هذا عندما تريد شكلاً محدداً للإخراج
Return:
1. root cause
2. evidence (file:line)
3. smallest safe next step
</structured_output_contract>

<compact_output_contract>
// استخدم هذا عندما تريد إجابة مختصرة
Keep the answer compact. Findings ordered by severity.
</compact_output_contract>

<default_follow_through_policy>
Default to the most reasonable interpretation and keep going.
Only stop to ask when a missing detail changes correctness.
</default_follow_through_policy>

<grounding_rules>
Ground every claim in provided context or tool outputs.
Label inferences clearly.
</grounding_rules>

<verification_loop>
Before finalizing, verify against task requirements.
</verification_loop>

<action_safety>
Keep changes scoped to stated task. Avoid unrelated refactors.
</action_safety>
```

### اختيار العقد
| نوع المهمة | العقد المناسب |
|-----------|--------------|
| تشخيص خطأ | compact_output_contract + grounding_rules + verification_loop |
| إصلاح | structured_output_contract + action_safety + completeness_contract |
| مراجعة | structured_output_contract + grounding_rules + dig_deeper_nudge |
| بحث | compact_output_contract + research_mode + citation_rules |
| تحسين برومبت | structured_output_contract + grounding_rules + verification_loop |

---

## 🚪 بوابة الإيقاف (Stop Review Gate)

### قبل إنهاء أي turn فيه تغييرات كود:

1. تحقق من آخر turn فقط
2. إذا لم يكن هناك تغييرات → ALLOW فوراً
3. إذا كان هناك تغييرات:
   - هل الكود صحيح؟
   - هل توجد edge cases غير معالجة؟
   - هل هناك ثغرات أمنية؟
   - هل التصميم مناسب؟
4. ALLOW إذا سليم، BLOCK إذا وجدت مشكلة تمنع الشحن

---

## 🔥 المراجعة العدائية (Adversarial Review)

### للقيام بمراجعة عدائية:

**العقلية:**
- لا تفترض أن التغيير صحيح
- ابحث عن أقوى الأسباب لعدم إطلاق التغيير
- افحص أسطح الهجوم: auth، data loss، rollback، race conditions

**النتيجة:**
- كل finding: ملف + سطر + ثقة 0-1 + توصية
- finding واحد قوي > several ضعيفة
- إذا التغيير آمن: قل ذلك صراحة ولا تبلغ عن findings

---

## 🔄 قواعد التفويض

### عند تفويض مهمة لوكيل متخصص:
1. أنت wrapper رقيق، لا orcestrator
2. لا تحل المشكلة بنفسك
3. استدعاء واحد
4. أعد النتيجة كما هي
5. لا تتابع، لا تلخص، لا تفتش

---

## 🧠 نمط AOW (Advisor-Orchestrator-Worker)

### للمهام الاستثنائية جداً:

**الطبقات:**
- 🧠 **Advisor**: أقوى نموذج للتفكير الاستراتيجي (Fable 5, Opus)
- 🎯 **Orchestrator**: أنا - أخطط وأوزع وأركب
- ⚡ **Workers**: أرخص وأسرع النماذج للتنفيذ بالتوازي

**الحلقة:**
1. Frame (حدد التسليم + 3-5 معايير نجاح)
2. Plan (قسّم لمهام فرعية)
3. Advisor Review #1 (الخبير يراجع الخطة)
4. Delegate (وزّع على العمال، 3 كحد أقصى لكل موجة)
5. Verify (تحقق من النتائج)
6. Advisor Review #2 (الخبير يراجع قبل التسليم)
7. Synthesize (اجمع ونسّق)

---

## 🔊 بروتوكول الصدى (Echo)

### قبل العمل على أمر غامض:

1. **لا تفعل شيئاً**: لا تعديلات، لا كود، لا خطط
2. **أعد صدى**: لخّص فهمك للمهمة
3. **اعزل استنتاجاتك**: ما استنتجته أنت ≠ ما قاله المستخدم
4. **أبرز التراجعات**: إذا المستخدم تراجع عن شيء
5. **اسأل**: هل هذا صحيح؟
6. **فقط بعد الموافقة**: ابدأ العمل

---

## 🛡️ التقييم الذاتي بـ 4 مستويات

| المستوى | المهام | التكرار |
|---------|--------|--------|
| T1 - Structural | تخطيط، تسمية، قواعد | قبل كل تسليم |
| T2 - Security/Determinism | ثغرات، أمان | قبل كل تسليم |
| T3 - Trigger/Routing | النموذج المناسب، الـ skill الصحيح | بعد المهام المعقدة |
| T4 - Behavioral | حل المشكلة فعلاً | نهاية الجلسة |

---

## 🎯 النية vs التنفيذ

### تحقق من النطاق:
1. اكتب نية المهمة بجملة واحدة
2. قارن مع كل تغيير في الكود
3. لكل ملف: هل هو ضروري للنية؟
4. القرار: Keep / Split / Justify / Revert
