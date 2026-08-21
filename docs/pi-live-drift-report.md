# Pi Live Drift Report

**تاريخ الفحص:** 2026-08-21

## نطاق الفحص

تم فحص الأرشيف المنقح `pi-live-export-20260821-150645.tar.gz` قراءةً فقط. اجتاز الأرشيف فحص سلامة المسارات، ولم يحتوي على `auth.json` أو `models-store.json` أو `sessions/` أو `.env` أو ملفات PID أو سجلات تشغيل، كما لم تظهر فيه أنماط مفاتيح معروفة. لم تُقرأ أو تُخزن القيم السرية الخام.

## النتائج الرقمية

| القياس | النتيجة |
|---|---:|
| ملفات الأرشيف | 907 |
| ملفات `nova/` | 150 |
| Plugins | 15 |
| ملفات Runtime Adapter داخل `nova/` | 0 |
| Extensions في الحزمة | `penpot-mcp.ts` فقط |
| اختلافات شجرة Nova عن المستودع | لا يوجد |
| اختلاف امتداد Penpot عن المستودع | لا يوجد |

## الانحرافات بين الحي والمستودع

| الإعداد | Pi الحي | المستودع | التفسير |
|---|---|---|---|
| `defaultProvider` | `opencode` | `freemodel` | لم يُعتمد التغيير في الحي |
| `defaultModel` | `hy3-free` | `gpt-5.4-mini` | لا يُبدّل قبل اختبار المزود |
| `modelRouting.defaultProvider` | `nvidia` | `freemodel` | تعارض قديم في الحي |
| `modelRouting.fallbackProvider` | `cloudflare-workers-ai` | `freemodel` | يحتاج اختبارًا قبل التغيير |
| `instructions.files` | `/root/.pi/...` | `$PI_HOME/...` | المسار الحي أبقى الصيغة المؤكدة |
| AOW models | `claude-fable-5` / `sonnet` / `gemini-3.5-flash` | نماذج موجودة في القائمة المنقحة | القيم الحية القديمة غير مثبتة في `models.json` |
| مفاتيح مزودي النماذج | قيم حرفية في البيئة الحية | مراجع متغيرات بيئة | يحتاج تدويرًا واختبارًا منفصلًا |

## Nova Runtime

لا يوجد في الحزمة الحية ملف `nova-runtime.ts` أو `coordinator.ts` أو `loader.ts` أو `agents.ts` أو أي ملف تنفيذي داخل `nova/`. لذلك لا توجد أدلة على تنفيذ Orchestrator أو Event Bus خاص بـ Nova. ملفات `workflow.json` و`events.json` وملفات Plugins هي عقود Blueprint فقط.

النتيجة التشغيلية المعتمدة هي:

> **ECC Active — Nova Passive — Runtime Adapter Missing**

## القرار

يصبح مستودع `pi-config-backup` مصدر الحقيقة للتكوين القابل للإصدار. تبقى `/root/.pi` نسخة نشر حية للمقارنة والاختبار، ولا تُنسخ منها الأسرار أو الجلسات. لا تُطبّق تغييرات إعدادات النماذج على Pi الحي في هذه المرحلة، ولا يبدأ Runtime Adapter قبل تثبيت مواصفة واحدة ونجاح Spike رسمي لاستدعاء الوكلاء.

## الإجراءات المؤجلة

تدوير المفاتيح، اختبار `freemodel/gpt-5.4-mini`، مواءمة `modelRouting` وAOW، ثم بناء Runtime Adapter هي مراحل مستقلة. كل مرحلة تحتاج نسخة احتياطية، اختبارًا، وتراجعًا واضحًا. لا يجوز جمعها في تعديل واحد غير قابل للعزل.
