# Pi Config Backup — Operating Instructions

## المهمة الأساسية

أنت تعمل داخل مستودع `4zobir89-lab/pi-config-backup`. هذا المستودع هو **مصدر الحقيقة للتكوين القابل للإصدار**. أما `/root/.pi` أو `$PI_HOME` فهو نسخة تشغيلية حية يجب التعامل معها كـ deployment target، وليس كمصدر تعديلات عشوائية.

هدفك هو إبقاء Pi/ECC منظمًا وقابلًا للتراجع، وتطبيق التحديثات الآمنة تلقائيًا من هذا المستودع، مع منع تسريب الأسرار وعدم الادعاء بأن Nova تعمل Runtime قبل إثبات ذلك.

## الحالة المعتمدة

> **ECC Active — Nova Passive — Runtime Adapter Missing**

طبقة `pi/agent/nova/` الحالية هي Blueprint مكوّن من JSON/YAML/Markdown وPlugins وعقود Schemas. لا يوجد حاليًا Runtime Adapter أو Orchestrator تنفيذي لـ Nova داخل Pi. لذلك لا تقل إن Nova تعمل فعليًا لمجرد وجود `nova.enabled` أو `workflow.json`.

## الترتيب الإلزامي عند بدء العمل

عند فتح المستودع، نفّذ قراءة فقط بالترتيب التالي:

```bash
pwd
git remote -v
git status --short --branch
git log -3 --oneline --decorate
sed -n '1,240p' docs/source-of-truth.md
sed -n '1,260p' docs/pi-live-drift-report.md
python3 scripts/validate_nova.py
```

بعد ذلك افحص نسخة Pi الحية باستخدام `PI_HOME`، من دون طباعة `models.json` الخام أو `auth.json` أو محتويات الجلسات:

```bash
PI_HOME="${PI_HOME:-$HOME/.pi}"
[ -d /root/.pi ] && PI_HOME=/root/.pi
printf 'PI_HOME=%s\n' "$PI_HOME"
find "$PI_HOME/agent" -maxdepth 1 -mindepth 1 -printf '%f\n' | sort
```

## سياسة مصدر الحقيقة

| المجال | المصدر |
|---|---|
| تعليمات Pi وECC | `pi/agent/` داخل المستودع |
| Nova Blueprint | `pi/agent/nova/` داخل المستودع |
| الإعدادات التشغيلية المقترحة | `pi/agent/settings.json` داخل المستودع، بعد اختبارها |
| تعريفات النماذج | `pi/agent/models.json` داخل المستودع، مع مراجع بيئية فقط |
| نسخة التشغيل | `$PI_HOME/agent/` |
| الأسرار والجلسات | خارج GitHub وخارج مخرجات الوكيل |

إذا تعارضت نسخة Pi الحية مع المستودع، سجّل الفرق أولًا. لا تنشئ مصدر حقيقة ثالثًا، ولا تنسخ التغييرات الحية إلى المستودع تلقائيًا.

## المزامنة التلقائية المسموحة

يمكنك تطبيق المزامنة الآمنة تلقائيًا من المستودع إلى Pi الحي للملفات غير الحساسة فقط. استخدم:

```bash
bash scripts/pi-safe-sync.sh --safe
```

هذه العملية تنشئ نسخة احتياطية محلية قبل التعديل، ثم تزامن تعليمات ECC والقواعد والمهارات والأوامر والامتدادات وطبقة Nova وملفات الأدوات. لا تستخدم `rsync --delete`، ولا تحذف ملفات حية خارج الملفات التي يملكها المستودع.

بعد المزامنة، شغّل:

```bash
python3 scripts/validate_nova.py
```

ثم اختبر Pi بجلسة جديدة واكتب نتيجة الاختبار في تقرير، من دون تسجيل أي prompt خاص أو مفتاح.

## إعدادات النماذج والأسرار

لا تنسخ `settings.json` أو `models.json` إلى Pi الحي تلقائيًا. هذه الملفات حساسة وقد تغيّر المزود الافتراضي أو توقف Pi إذا لم تكن متغيرات البيئة متوفرة.

لا تطبع أو تعرض أو تحفظ أي قيمة من الحقول التالية: `apiKey` و`token` و`secret` و`password` و`authorization` و`credential`. لا تطلب من المستخدم إرسالها في المحادثة.

لا تطبق إعدادات النماذج إلا بعد تحقق كل الشروط التالية:

1. وجود `FREEMODEL_API_KEY` و`DAHL_API_KEY` و`NVIDIA_API_KEY` في بيئة التشغيل عند الحاجة.
2. تشغيل فحص JSON وفحص المراجع البيئية.
3. أخذ نسخة احتياطية محلية مشفرة الصلاحيات أو محمية بامتيازات المستخدم.
4. تطبيق `settings.json` و`models.json` معًا لتجنب عدم التوافق.
5. تشغيل اختبار Pi فعلي بنجاح.
6. إبقاء أمر Rollback واضحًا وعدم حذف النسخة الاحتياطية.

إذا غاب شرط واحد، توقف وقدم تقريرًا، ولا تستبدل الملفات الحساسة.

## Nova Runtime Adapter

لا تبدأ بناء Runtime Adapter تلقائيًا. قبل أي تنفيذ يجب أن توجد مواصفة معتمدة وSpike يثبت آلية رسمية لاستدعاء الوكلاء من Pi v0.84.2. إذا لم توجد `runAgent` أو `dispatchAgent` أو آلية رسمية موثقة، توقف وارفع ADR؛ لا تستخدم Slash Command برمجيًا أو workaround غير مثبت.

لا تعدّل `dist/` أو Pi Core. أي Runtime مستقبلي يجب أن يكون Extension معزولًا وقابلًا للحذف، ويجب أن يملك اختبارات idempotency وArtifact gating وpermissions وretry وRollback.

## قواعد التغيير

قبل أي تعديل، اكتب في تقرير داخلي: الهدف، الملفات المتأثرة، المخاطر، وخطة التراجع. نفّذ التغييرات في فرع منفصل، ثم شغّل الاختبارات، ثم راجع `git diff --check`، ثم استخدم Conventional Commit.

لا ترفع إلى `main` إلا بعد نجاح التحقق. لا ترفع ملفات `auth.json` أو `models-store.json` أو `sessions/` أو `.env` أو `trust.json` أو ملفات PID والسجلات أو أي أسرار. إذا اكتشفت سرًا، أوقف العملية واطلب تدويره؛ لا تنسخه ولا تطبعه.

## صيغة التقرير النهائي

عند الانتهاء، أعد تقريرًا بالعربية يتضمن: ما تم فحصه، ما تم تغييره، ما لم يتم تغييره، نتيجة الاختبارات، مسار النسخة الاحتياطية، commit، وما بقي مؤجلًا. فرّق دائمًا بين `ACTIVE` و`PASSIVE` و`UNSUPPORTED`، ولا تخلط Blueprint مع Runtime.
