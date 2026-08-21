# Nova-compatible Architecture

## الهدف

الهدف هو تحويل نسخة إعدادات Pi إلى أساس قابل للنمو لمنصة تطوير برمجيات متعددة الوكلاء. المعمارية الجديدة لا تدّعي أن Pi أصبح منصة SaaS مكتملة؛ بل توفر عقود التشغيل التي تمنع الفوضى عند إضافة التنفيذ الفعلي.

## المكونات

| المكوّن | المسؤولية | مصدر الحقيقة |
|---|---|---|
| Orchestrator | إدارة الحالة والتفويض والتجميع | `pi/agent/nova/workflow.json` |
| Event System | نقل الأحداث وإعادة المحاولة والتدقيق | `pi/agent/nova/events.json` |
| Project Memory | الملفات والقرارات والتصميم والكود | `project-memory.schema.json` |
| Agent Memory | ذاكرة الوكيل والجلسة | `agent-memory.schema.json` |
| Knowledge Memory | أفضل الممارسات والتوثيق والأنماط | `knowledge-memory.schema.json` |
| Artifact System | نتائج قابلة للإصدار والتحقق | `artifact.schema.json` و`artifact-catalog.json` |
| Tool Layer | أدوات خارجية بسياسة deny-by-default | `tool-registry.json` و`permissions.json` |

## دورة الحالة

تبدأ الدورة بـ `PROJECT_CREATED`، ثم تمر بالاكتشاف والتخطيط والمعمارية والتصميم والتطوير والدمج والمراجعة الأمنية وضمان الجودة والنشر والتحسين. لا يعني اسم الحدث أن الانتقال ناجح تلقائيًا؛ النجاح يتطلب Artifacts المطلوبة ونتيجة تحقق مسجلة.

## إضافة وكيل

ينشئ المطور مجلدًا تحت `pi/agent/nova/plugins/<agent-id>`، ثم يضيف تعريفه إلى `agent-registry.json`، ويحدد صلاحياته، ويضيف Prompt وSchemas وValidators. يجب أن يكون الوكيل قابلاً لإعادة التشغيل بأمان، وألا يقرأ أسرارًا مباشرة، وألا ينفذ كتابة خارجية دون موافقة.
