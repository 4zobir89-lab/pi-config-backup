# 🎨 Penpot MCP Server - دليل التشغيل

## الحالة الحالية

✅ **تم الإعداد:**
- ملف المعرفة: `/root/.pi/agent/knowledge/penpot.md`
- المهارة: `/root/.opencode/skills/penpot-integration/SKILL.md`
- التفعيل التلقائي في: `/root/.pi/agent/APPEND_SYSTEM.md`
- ملفات التشغيل: `/root/.pi/penpot-mcp/`

⚠️ **ملاحظة:** تشغيل MCP Server على هذا الجهاز بطيء بسبب الشبكة.

---

## البدائل للتشغيل

### البديل 1: تشغيل على جهاز آخر (مُوصى به)
```bash
# على جهازك المحلي (PC/Mac)
git clone https://github.com/penpot/penpot.git --branch mcp-prod-2.14.1 --depth 1
cd penpot/mcp
./scripts/setup
pnpm run bootstrap
```

### البديل 2: استخدام Docker
```bash
# تشغيل Penpot الكامل
git clone https://github.com/penpot/penpot.git
cd penpot/docker
docker compose up -d
# الوصول: http://localhost:9001
```

### البديل 3: النسخة السحابية (أسهل)
```bash
# لا حاجة للتثبيت - استخدم design.penpot.app
# https://design.penpot.app
```

---

## كيفية الاتصال بـ MCP Server

### بعد تشغيل الخادم:
```bash
# 1. شغّل MCP Server
/root/.pi/penpot-mcp/start.sh

# 2. اتصل بـ Claude Code
claude mcp add penpot -t http http://localhost:4401/mcp

# 3. في Penpot (المتصفح)
#    → افتح ملف تصميم
#    → Plugins → حمّل http://localhost:4400/manifest.json
#    → اضغط "Connect to MCP server"
```

---

## ما يمكن فعله مع Penpot MCP

| الطلب | الإجراء |
|-------|----------|
| "شغّل Penpot MCP" | يبدأ الخادم تلقائياً |
| "حلّل هذا التصميم" | يتصل بالـ MCP ويقرأ البيانات |
| "أنشئ واجهة من وصف" | ينشئ عناصر عبر MCP |
| "صدر كود من التصميم" | يقرأ ويحول إلى React/CSS |
| "حدث Design Tokens" | يعدّل عبر MCP |

---

## المنافذ

| الخدمة | المنفذ | الرابط |
|--------|--------|--------|
| MCP Server | 4401 | http://localhost:4401/mcp |
| Plugin Server | 4400 | http://localhost:4400 |
| WebSocket | 4402 | للاتصال بالـ Plugin |

---

## أوامر التشغيل

```bash
# بدء التشغيل
/root/.pi/penpot-mcp/start.sh

# إيقاف
/root/.pi/penpot-mcp/stop.sh

# حالة
/root/.pi/penpot-mcp/status.sh
```

---

## حلول المشاكل

### المشكلة: بطيء في التحميل
**الحل:** استخدم proxy أو شغّل على جهاز آخر

### المشكلة: المنفذ مشغول
**الحل:**
```bash
# ابحث عن العملية المشغّلة
lsof -i :4401
# أوقفها
kill -9 <PID>
```

### المشكلة: فشل الاتصال
**الحل:**
```bash
# تحقق من حالة الخادم
/root/.pi/penpot-mcp/status.sh
# أعد التشغيل
/root/.pi/penpot-mcp/stop.sh
/root/.pi/penpot-mcp/start.sh
```

---

## روابط مفيدة

| المورد | الرابط |
|--------|--------|
| Penpot | https://penpot.app |
| التوثيق | https://help.penpot.app |
| MCP Docs | https://penpot.app/penpot-mcp-server |
| GitHub | https://github.com/penpot/penpot |
