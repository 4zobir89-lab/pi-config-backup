# ECC Quick Reference Card v2.1 🚀

## ⚡ القواعد الذهبية (إلزامي)

### ❌ لا تفعل:
- لا كود بدون تخطيط
- لا كود بدون اختبارات
- لا دوال > 50 سطر
- لا ملفات > 800 سطر
- لا hardcode
- لا تتجاهل السياق
- لا تعمل وحدك للمهام المعقدة

### ✅ افعل دائماً:
- اسأل أولاً ← خطط أولاً ← اختبر أولاً
- راقب السياق (/compact عند < 30%)
- استخدم سوَرْم للمهام المستقلة
- تعلّم من كل جلسة
- طوّر تعليماتك
- وجّه النماذج بذكاء
- راجع دائماً ← Conventional Commits

---

## 🔄 الورك فلو المتقدم (إلزامي)

```
1.  🎯 Plan      → planner agent
2.  📚 Research  → search-first / Context7
3.  🔬 TDD       → tdd-guide agent
4.  🧠 Context   → راقب /compact
5.  🐝 Swarm     → وزّع المهام المستقلة
6.  🔍 Review    → code-reviewer agent
7.  🔒 Security  → security-reviewer agent
8.  📝 Commit    → Conventional Commits
9.  🧠 Learn     → instincts + growth log
10. 🔧 Improve   → طوّر التعليمات
```

---

## 🎯 استخدام الوكلاء (إلزامي)

```
ميزة معقدة        → planner
كتب/عدّل كود      → code-reviewer
إصلاح خلل         → tdd-guide
قرار معماري        → architect
كود حساس          → security-reviewer
مهمة متعددة الطبقات → swarm (عدة وكلاء)
مراجعة شاملة       → parallel (security + code + tdd)
تحسين التعليمات    → self-improvement workflow
```

---

## 🧠 إدارة السياق (جديد!)

```
متبقي < 30% → /compact فوراً
متبقي < 15% → توقف واسأل المستخدم
متبقي < 5%  → /clear وجلسة جديدة
كل 5-10 تبادلات → /compact وقائي
لا تحمل مهارات غير ضرورية
```

---

## 🐝 السوَرْم (جديد!)

```
قسّم المهمة → وزّع على وكلاء → اشتغل بالتوازي
→ كل وكيل في branch مستقل → اختبر كل جزء → ادمج

منسّق يخطط ويوزع ← Workers ينفذون ← Merger يدمج
```

---

## 🎯 توجيه النماذج (مختبرة ✅)

```
روتين/بحث/Bash     → gpt-5.4-mini (freemodel) مجاني
برمجة/اختبارات     → big-pickle (opencode) مدفوع
هندسة/أخطاء معقدة  → big-pickle (opencode) مدفوع
مراجعة كود         → big-pickle (opencode) مدفوع

التبديل: /model gpt-5.4-mini  أو  /model big-pickle
```

---

## 📝 Conventional Commits (إلزامي)

```
<type>: <description>
Types: feat, fix, refactor, docs, test, chore, perf, ci
```

---

## 🔒 الأمان (إلزامي)

```
- لا مفاتيح hardcode
- تحقق من المدخلات
- منع SQL injection/XSS
- Rate limiting
- مراجعة أمنية قبل كل commit
```

---

## 📊 جودة الكود (إلزامي)

```
- دوال < 50 سطر
- ملفات < 800 سطر
- تغوص < 4 مستويات
- تغطية 80%+
- KISS / DRY / YAGNI
```

---

## 📐 بناء البرومبتات (جديد من Codex Plugin!)

```xml
<task>المهمة</task>
<structured_output_contract>شكل الإخراج</structured_output_contract>
<grounding_rules>استند للأدلة</grounding_rules>
<default_follow_through_policy>أكمل أو اسأل</default_follow_through_policy>
<verification_loop>تحقق قبل التسليم</verification_loop>
```

---

## 🚪 بوابة الإيقاف (جديد!)

```
بعد كل turn فيه كود: ALLOW أو BLOCK
BLOCK فقط لمشاكل حقيقية
ALLOW فوراً إذا لا يوجد تغيير
```

---

## 🔥 المراجعة العدائية (جديد!)

```
ابحث عن: auth, data loss, race, rollback
كل finding: ملف + سطر + ثقة + توصية
finding واحد قوي > several ضعيفة
```

---

## 🔄 التفويض للوكلاء (جديد!)

```
مرّر الطلب ← لا تحلل ← أعد النتيجة كما هي
wrapper رقيق، ليس orchestrator
```

---

## 📦 عقود الإخراج (جديد!)

```
التشخيص: compact (سبب + دليل + خطوة)
المراجعة: structured (findings + severity)
الإصلاح: structured (ملخص + ملفات + مخاطر)
```

---

## 🔄 نمط AOW (جديد من Awesome LLM Apps!)

```
🧠 Advisor: استراتيجية + مخاطر (لا ينفذ)
🎯 Orchestrator: أنا — أخطط وأوزع
⚡ Workers: ينفذون بالتوازي

الحلقة: Frame → Plan → Advisor → Delegate → Verify → Advisor → Synthesize
```

---

## 🔊 الصدى (Echo) (جديد!)

```
1. لا تفعل شيئاً
2. أعد صدى: لخّص فهمك
3. استنتاجاتك ≠ كلام المستخدم
4. اذكر التراجعات
5. اطلب الموافقة → ابدأ
```

---

## 🛡️ التقييم بـ 4 مستويات (جديد!)

```
T1-هيكل T2-أمان T3-محفزات T4-سلوك
قبل التسليم: T1+T2
نهاية الجلسة: T4+Growth Log
```

---

## 🎯 النية vs التنفيذ (جديد!)

```
حدد نية → قارن مع التغييرات → Keep/Split/Justify/Revert
```

---

## 📡 وكلاء دائمون (جديد!)

```
مهمة واحدة فقط → تقارير 30 ثانية → لا تعديل بدون إذن
```

---

## 🔗 MCP & RAG (جديد!)

```
MCP: Browser/GitHub/Notion للأدوات الخارجية
RAG: Basic/Agentic/CRAG/Hybrid حسب الدقة المطلوبة
```

---

**تذكير: هذه التعليمات إلزامية وليست اقتراحات**
**آخر تحديث: 2026-07-30 | مستوحى من jcode + Codex Plugin + Awesome LLM Apps**
