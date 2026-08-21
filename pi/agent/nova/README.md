# Nova-compatible Pi

هذه الطبقة تجعل Pi يعمل كنظام **Event-Driven متعدد الوكلاء** بدل مجموعة تعليمات متفرقة. المنسق يملك حالة سير العمل، والوكلاء Plugins مستقلة، والنتائج Artifacts قابلة للتتبع، والذاكرة مقسمة إلى Project وAgent وKnowledge Memory.

## نقطة الحقيقة

يُعد `agent-registry.json` سجل الوكلاء، و`events.json` عقد الأحداث، و`workflow.json` مخطط الحالة العام، و`permissions.json` سياسة الصلاحيات، و`tool-registry.json` سجل الأدوات. لا تضف وكيلًا جديدًا قبل إضافة Plugin كامل له `agent.json` و`instructions.md` و`tools.json` و`memory.json` و`schemas/` و`validators/`.

## التشغيل

يبدأ المشروع بحدث `PROJECT_CREATED`. ينتقل المنسق بين المراحل العشر بعد تحقق Artifacts، ويعيد المهمة إلى المسار المناسب عند `TEST_FAILED` أو `FIX_REQUIRED`. عمليات النشر والكتابة الخارجية وتدوير الأسرار تتطلب موافقة صريحة.

## التحقق

شغّل `python3 scripts/validate_nova.py` من جذر المستودع. التحقق يفحص JSON، وتطابق السجل مع Plugins، وتسلسل الأحداث، والمراجع غير الصالحة للنماذج، ومؤشرات الأسرار.
