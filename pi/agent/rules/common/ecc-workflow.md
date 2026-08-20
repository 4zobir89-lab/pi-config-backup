# ECC Workflow Integration (Pi v0.80.6)

## Overview

هذا الملف يوضح كيفية تطبيق ECC بشكل صارم في بيئة Pi.

## الورك فلو الأساسي

### 1. Plan Phase (التخطيط)

**عندما تطلب ميزة معقدة:**
```
المستخدم: أضف ميزة مصادقة OAuth

الوكيل المطلوب: planner

النتيجة:
- تقسيم المهام إلى خطوات صغيرة
- تحديد التبعيات
- تحديد ملفات الكود المتأثرة
- تحديد الاختبارات المطلوبة
```

**الخطوات:**
1. اقرأ المتطلبات بعناية
2. حدد المكونات الرئيسية
3. اكتب خطة التنفيذ
4. حدد نقاط الاختبار

### 2. TDD Phase (الاختبارات أولاً)

**عندما تكتب كوداً جديداً أو تصلح خللاً:**
```
المستخدم: أصلح خطأ في حساب التشابه

الوكيل المطلوب: tdd-guide

الخطوات:
1. RED: اكتب اختبار يفشل
2. GREEN: اكتب أقل كود ينجح
3. REFACTOR: حسّن مع الحفاظ على التغطية
```

**القواعد:**
- لا تكتب كوداً بدون اختبار
- تأكد من فشل الاختبار أولاً
- اكتب أقل كود ينجح
- حافظ على تغطية 80%+

### 3. Review Phase (المراجعة)

**بعد كتابة/تعديل الكود:**
```
المستخدم: اكتب كود معالجة للبيانات

الوكيل المطلوب: code-reviewer

التحقق من:
- [ ] جودة الكود
- [ ] الأمان
- [ ] الأداء
- [ ] التغطية
- [ ] التوثيق
```

### 4. Commit Phase (التثبيت)

**تنسيق الإلتزام (إلزامي):**
```
<type>: <description>

Types: feat, fix, refactor, docs, test, chore, perf, ci
```

**أمثلة صحيحة:**
```
feat: add OAuth authentication
fix: resolve memory leak
refactor: extract validation utils
docs: update API documentation
test: add unit tests
chore: update dependencies
perf: optimize queries
ci: add GitHub Actions
```

## استخدام الوكلاء التلقائي

### لا تنتظر طلب المستخدم

```
1. طلب ميزة معقدة     → planner
2. كتابة/تعديل كود    → code-reviewer
3. إصلاح خلل / ميزة جديدة → tdd-guide
4. قرار معماري        → architect
5. كود حساس أمنياً    → security-reviewer
```

### Parallel Execution

**المهام المستقلة → تنفيذ متوازي:**

```markdown
# مثال: مراجعة شاملة
تشغيل بالتوازي:
1. security-reviewer: تحليل أمني
2. code-reviewer: مراجعة جودة
3. tdd-guide: التحقق من التغطية
```

## جودة الكود

### المقاييس الإلزامية

- دوال صغيرة (<50 سطر)
- ملفات مركزة (<800 سطر)
- لا تغوص عميق (>4 مستويات)
- معالجة أخطاء في كل مستوى
- لا قيم hardcode
- معرفات مقروءة وواضحة

### مبادئ KISS/DRY/YAGNI

- **KISS**: ابسط حل يعمل فعلاً
- **DRY**: لا تكرر نفس الكود
- **YAGNI**: لا تبني ميزات لم تطلب بعد

## أمان (إلزامي)

### قبل أي commit

- [ ] لا مفاتيح hardcode
- [ ] تحقق من كل مدخلات المستخدم
- [ ] منع SQL injection
- [ ] منع XSS
- [ ] تفعيل CSRF
- [ ] التحقق من Auth
- [ ] Rate limiting
- [ ] لا تسريب بيانات حساسة

### استجابة الأمان

```
STOP → security-reviewer → إصلاح CRITICAL → تدوير المفاتيح → مراجعة شاملة
```

## إعدادات Pi

### إعدادات النموذج

```json
{
  "model": "sonnet",
  "env": {
    "MAX_THINKING_TOKENS": "10000",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"
  }
}
```

### استخدام يومي

| الأمر | متى نستخدمه |
|--------|-------------|
| `/model sonnet` | المهام العادية |
| `/model opus` | معمارية معقدة، تصحيح أخطاء |
| `/clear` | بين مهام غير مترابطة |
| `/compact` | عند نقاط الانقطاع المنطقية |
| `/cost` | مراقبة الإنفاق |

## 🧠 مرحلة إدارة السياق (Context Phase)

**راقب سياقك باستمرار - هو أثمن مورد عندك.**

```markdown
## متى تحتاج ضغط سياق:
1. بعد 5-10 تبادلات معقدة → /compact
2. عند ملاحظة تباطؤ في الردود
3. قبل بدء مهمة جديدة تماماً
4. عند التبديل بين مشاريع مختلفة

## نصائح:
- /compact ≠ /clear (الضغط يحافظ على الجوهر)
- استخدم /clear فقط بين المهام غير المترابطة
- ابدأ جلسة جديدة إذا كان السياق < 15%
```

---

## 🐝 مرحلة السوَرْم (Swarm Phase)

**للمهام المعقدة: وزّع العمل على وكلاء متخصصين.**

```markdown
## متى نستخدم سوَرْم:
- المهمة تحتوي 3+ طبقات (مثلاً: API + UI + DB)
- تحتاج تحليلات من زوايا متعددة
- بناء مشروع كامل من الصفر

## هيكل السوَرْم:

منسّق (Coordinator) ← يخطط ويوزع
├── Worker 1: Backend (API, DB)
├── Worker 2: Frontend (UI, State)
├── Worker 3: Tests (Integration, E2E)
└── Worker 4: Docs (وثائق)

## قواعد:
1. كل وكيل يشتغل في فرع منفصل أو worktree
2. توثيق كل تغيير
3. اختبار كل وحدة قبل الدمج
4. المنسق يراجع كل PR قبل الدمج
```

---

## 🧠 مرحلة التعلم (Learning Phase)

**في نهاية كل جلسة: استخرج ما تعلمته.**

```markdown
## نهاية الجلسة:
1. تأكد من capture instincts (Continuous Learning v2)
2. اكتب Growth Log لو كان هناك درس مهم
3. سجّل ADR لأي قرار معماري
4. خزّن أي patterns اكتشفتها

## بداية الجلسة:
1. استرجع instincts من الجلسات السابقة
2. راجع ADRs المعلقة
3. اقرأ آخر memory entries إذا كانت متاحة
```

---

## 🔧 مرحلة التطوير الذاتي (Self-Improvement)

**حسّن تعليماتك وأدواتك باستمرار.**

```markdown
## متى نطور أنفسنا:
- لاحظت workflow بطيء
- كررت نفس الخطوات 3+ مرات
- يوجد أداة أو skill جديدة مفيدة

## كيف:
1. لاحظ المشكلة
2. ابحث عن حل أفضل
3. خطط التحسين
4. نفّذ
5. قِس النتيجة

## آمن:
- أضف rules جديدة
- حسّن المهارات الموجودة
- طوّر التعليمات

## ممنوع:
- تغيير قواعد الأمان
- إزالة enforcement
- تعطيل TDD
```

---

## 🎯 مرحلة التوجيه الذكي (Model Routing)

**استخدم النموذج المناسب لكل مهمة - بناءً على اختبارات فعلية.**

### ✅ النماذج المتوفرة فعلاً:

```
🥇 opencode/big-pickle (200k ctx) - الموصى به للبرمجة
   - المصدر الأساسي لكل مهام التطوير
   - يدعم reasoning + vision
   - مدفوع لكن متضمن في الاشتراك

🥈 freemodel/gpt-5.4-mini (128k ctx) - البديل المجاني
   - يعمل حالياً - مختبر
   - ممتاز للمهام الروتينية
   - مجاني 100%

🥉 freemodel/gpt-5.6-sol (128k ctx) - بديل مجاني أقوى
   - يعمل حالياً - مختبر
   - ممتاز للبرمجة الخفيفة
   - مجاني 100%

📋 باقي النماذج المتاحة: gpt-5.6-luna, gpt-5.5, gpt-5.4 (freemodel)
```

### 🔴 نماذج غير متوفرة حالياً (لا تحاول استخدامها):

```
✗ dahl (Kimi K2.6, MiniMax M2.7) → token expired
✗ nvidia (GLM 5.2, Qwen 3.5)     → missing key / EOL
✗ cloudflare (GLM 5.2)            → needs paid plan
✗ gpt-5.3-codex                    → removed from API
```

### 🎯 جدول التوجيه المختبر:

| المهمة | الموديل | التكلفة |
|--------|---------|:-------:|
| قراءة/تحليل ملفات | gpt-5.4-mini | 🆓 |
| بحث سريع | gpt-5.4-mini | 🆓 |
| أوامر bash | gpt-5.4-mini | 🆓 |
| grep/بحث | gpt-5.4-mini | 🆓 |
| تعديلات بسيطة | gpt-5.4-mini | 🆓 |
| كتابة كود | big-pickle | 💰 |
| إصلاح أخطاء | big-pickle | 💰 |
| مراجعة كود | big-pickle | 💰 |
| اختبارات | big-pickle | 💰 |
| قرارات معمارية | big-pickle | 💰 |
| أخطاء معقدة | big-pickle | 💰 |
| أمان | big-pickle | 💰 |

### أوامر التبديل:
```bash
/model gpt-5.4-mini     # التبديل للمجاني
/model big-pickle       # التبديل للمدفوع
pi -p freemodel -m gpt-5.4-mini  # من الطرفية
```

---

## 📋 ورك فلو ECC الموسع

**ECC في Pi = 8 مراحل:**

```
1. 🎯 Plan        → planner agent
2. 📚 Research    → search-first, Context7, GitHub
3. 🔬 TDD          → tdd-guide agent
4. 🧠 Context      → /compact (مراقبة مستمرة)
5. 🐝 Swarm        → توزيع المهام المستقلة
6. 🔍 Review       → code-reviewer agent
7. 🔒 Security     → security-reviewer agent
8. 📝 Commit       → Conventional Commits
9. 🧠 Learn        → instincts + growth log
10. 🔧 Improve     → تطوير التعليمات
```

**هذه المراحل إلزامية للمهام المعقدة.**

---

## 📐 إضافة: نظام البرومبتات المحكمة (مستوحى من Codex Plugin)

### للمهام المعقدة، استخدم XML tags:

```xml
<task>المهمة بالضبط</task>
<structured_output_contract>شكل الإخراج</structured_output_contract>
<default_follow_through_policy>أكمل أم اسأل</default_follow_through_policy>
<grounding_rules>استند للأدلة فقط</grounding_rules>
<verification_loop>تحقق قبل التسليم</verification_loop>
<action_safety>لا تتعدى المهمة</action_safety>
```

### أنواع المهام والعقد المناسب:

| المهمة | العقد |
|--------|-------|
| تشخيص خطأ | compact_output + grounding + verification |
| إصلاح | structured_output + action_safety + completeness |
| مراجعة عادية | structured_output + grounding + dig_deeper |
| مراجعة عدائية | structured_output + operating_stance + attack_surface |
| بحث | compact_output + research_mode + citation_rules |

---

## 🚪 بوابة الإيقاف

```markdown
## بعد كل turn فيه تغييرات:
1. راجع آخر turn فقط
2. إذا لا تغييرات → ALLOW فوراً
3. إذا فيه تغييرات:
   - تحقق من الصحة
   - تحقق من الـ edge cases
   - تحقق من الأمان
4. ALLOW أو BLOCK
```

---

## 🔄 التفويض الصحيح للوكلاء

```markdown
## عند إرسال مهمة لوكيل:
✓ أنت wrapper رقيق
✓ استدعاء واحد
✓ أعد النتيجة كما هي
✗ لا تحلل المشكلة بنفسك
✗ لا تقرأ الملفات
✗ لا تتابع
✗ لا تلخص المخرجات
```

---

## 📦 عقود الإخراج (Output Contracts)

```markdown
## اختر العقد المناسب:
- التشخيص: compact (سبب + دليل + خطوة)
- المراجعة: structured (findings مرتبة حسب الخطورة)
- الإصلاح: structured (ملخص + ملفات + تحقق + مخاطر)
- البحث: compact (حقائق + استنتاجات + أسئلة مفتوحة)
```

---

## 🔄 نمط AOW (مستوحى من Awesome LLM Apps 129K⭐)

**Advisor-Orchestrator-Worker للمهام الاستثنائية:**

```
🧠 Advisor: أقوى نموذج (مثلاً Claude Fable 5)
   - استراتيجية، تحليل مخاطر
   - يُستشار فقط عند نقاط القرار الحرجة
   - لا ينفذ أبداً

🎯 Orchestrator: أنا
   - Hot path: plan, delegate, verify, synthesize
   - لا أعمل عمل العمال

⚡ Workers: أرخص النماذج (مثلاً Gemini 3.5 Flash)
   - Stateless، كل عامل في dir منفصل
   - يعملون بالتوازي (ماكس 3 لكل Wave)
   - فشل → retry ← Escalate
```

**الحلقة (Loop):**
1. Frame → 2. Plan → 3. Advisor Review → 4. Delegate → 5. Verify → 6. Advisor Review → 7. Synthesize

---

## 🔊 الصدى (Echo) - من Thinking Out Loud Skill

**قبل العمل على أمر غامض:**

```
1. لا تفعل شيئاً
2. لخّص فهمك (Echo): المهمة، استنتاجاتك، تراجعات
3. اعزل استنتاجاتك عن كلام المستخدم
4. اذكر كل تراجع لاحظته
5. المستخدم يوافق أو يصحح
6. فقط بعد الموافقة → ابدأ
```

---

## 🛡️ التقييم الذاتي بـ 4 مستويات

| المستوى | ماذا يفحص | متى |
|---------|----------|-----|
| T1 - Structural | هل اتبعت القواعد؟ | قبل كل تسليم |
| T2 - Security | هل هناك ثغرات؟ | قبل كل تسليم |
| T3 - Trigger | هل اخترت النموذج الصحيح؟ | بعد المهام المعقدة |
| T4 - Behavioral | هل حللت المشكلة فعلاً؟ | نهاية الجلسة |

---

## 🎯 النية vs التنفيذ

**تأكد أن كل تغيير ضروري:**

```
1. جملة نية واحدة (مثل: إصلاح null dereference)
2. قارن مع كل ملف تغير
3. هل كل ملف ضروري؟
4. قرار: Keep / Split / Justify / Revert
```

---

## 📚 أنماط RAG للاسترجاع الذكي

| المهمة | النمط |
|--------|-------|
| سؤال عن مستند | Basic RAG Chain |
| بحث متعدد المصادر | Agentic RAG |
| دقة عالية | Corrective RAG (CRAG) |
| محتوى متنوع | Hybrid Search RAG |
| وسائط متعددة | Multi-modal RAG |
| علاقات معقدة | Knowledge Graph RAG |

**القواعد:** اذكر المصدر، افصل حقائق ≠ استنتاجات، ارفض إذا الدليل ضعيف
