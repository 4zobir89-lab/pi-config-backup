# prompts.chat Library Integration

**المصدر:** https://github.com/f/prompts.chat
**آخر تحديث:** 2026-07-11
**الإحصائيات:** 1,001 prompt | 826 text | 153 structured | 21 image | 77 dev-specific

## كيفية الاستخدام

```bash
# البحث عن prompts
python3 /root/.pi/prompts-lib/query.py search "keyword"

# عرض جميع الفئات
python3 /root/.pi/prompts-lib/query.py list

# جلب prompt محدد
python3 /root/.pi/prompts-lib/query.py get "Linux Terminal"
```

## فئات الـ prompts الرئيسية

### لل-developers (77 prompt)
- Linux Terminal, JavaScript Console, SQL Terminal
- Ethereum Developer, UX/UI Developer
- Cyber Security Specialist, Web Design Consultant
- IT Architect, Tech Reviewer
- Developer Relations Consultant
- Scientific Data Visualizer, Tech Writer

### للتصميم (21 prompt - IMAGE)
- 3D Character Render, 3D City Prompt
- 3D Isometric Miniature, UI/UX Design
- Midjourney prompts, DALL-E prompts

### للإنتاجية (153 prompt - STRUCTURED)
- Email templates, Business plans
- Project plans, Meeting notes
- Research summaries

### للنصوص (826 prompt - TEXT)
- Translation, Writing, Teaching
- Marketing, Content creation
- Role-playing, Interview prep

## أمثلة سريعة

### للتطوير
```
Linux Terminal: "I want you to act as a linux terminal..."
JavaScript Console: "I want you to act as a javascript console..."
SQL Terminal: "I want you to act as a SQL terminal..."
```

### للتصميم
```
3D Character Render: prompts for creating 3D characters
UI/UX Developer: prompts for interface design
Web Design Consultant: prompts for web design
```

### للمحتوى
```
English Translator: "I want you to act as an English translator..."
Storyteller: "I want you to act as a storyteller..."
Content Writer: Various content writing prompts
```

## التحديث

لتحديث المكتبة:
```bash
curl -sL "https://raw.githubusercontent.com/f/prompts.chat/main/prompts.csv" > /root/.pi/prompts-lib/prompts.csv
```
