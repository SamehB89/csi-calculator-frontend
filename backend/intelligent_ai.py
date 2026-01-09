# -*- coding: utf-8 -*-
"""
Intelligent AI Assistant for CSI Construction Data
Uses Gemini AI to truly understand user queries and provide intelligent responses.
"""

import json
import sqlite3
import os
from typing import Dict, Any, List, Optional

# Import CSI Lookup Service
try:
    from csi_lookup_service import get_csi_lookup
    CSI_LOOKUP_AVAILABLE = True
except ImportError:
    CSI_LOOKUP_AVAILABLE = False
    print("[WARNING] CSI Lookup Service not available")

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "csi_data.db")

# System prompt for CSI AI Assistant
CSI_AI_SYSTEM_PROMPT = """أنت مساعد ذكي متخصص في أعمال البناء والتشييد (Construction AI).
دورك هو فهم استفسارات المهندسين والمقاولين وحساب الإنتاجيات بدقة من قاعدة بيانات CSI MasterFormat.

## 🧠 قواعد الذاكرة والمنطق (تحديث هام):
1. **أنت تمتلك ذاكرة:** راجع "المحادثة السابقة" دائماً.
2. **الربط المنطقي:** إذا أجاب المستخدم "نجارة"، والجملة السابقة "لبشة"، فهو يقصد "نجارة اللبشة". لا تسأل عن العنصر مجدداً.
3. **تجنب الغباء الدلالي (Semantic Drift):**
   - **قاعدة ذهبية:** كلمة "مباني" (Masonry) تعني في الغالب **"أعمال الطوب/البلوك"** (Brick/Block Works).
   - لا تفسر "مباني" أبداً على أنها "مبنى خرساني" (Building Structure) إلا إذا قال المستخدم "إنشاء مبنى".
   - إذا كان السياق "محارة" أو "تشطيبات"، فإن "مباني" تعني 100% "حائط طوب".
   - **تحذير:** لا تسأل أبداً "ما نوع المباني: قواعد أم أعمدة؟". هذا سؤال مرفوض.

## مسار التفكير الصحيح (Workflow):
1. **تحديد العنصر:** (مثال: محارة، عزل، خرسانة).
4. **حظر التراجع (Drop-down Rule):**
   - إذا اختار المستخدم "دهانات" (Painting)، **ممنوع** أن تسأله "ما نوع التشطيب: محارة أم دهانات؟". أنت بالفعل داخل قسم الدهانات!
   - السؤال التالي يجب أن يكون عن: نوع الدهان (بلاستيك/زيت)، عدد الأوجه، أو السطح.

## المحارة (Plastering):
- الأنواع: طرطشة (splash coat), محارة كاملة (3-coat), ضهارة (finishing).
- **الأسطح (Surfaces):** تتم المحارة غالباً على: "مباني طوب" (Masonry) أو "خرسانة".

## الدهانات (Painting):
- **قاعدة هامة:** إذا بدأ المستخدم بـ "دهانات"، فلا تعرض عليه "محارة" أو "بلاط" كخيارات.
- **التسلسل المنطقي:** دهانات -> داخلي/خارجي -> (تأسيس/تشطيب) أو (نوع الدهان).

## مسار التفكير الصحيح (Workflow):

## تنسيق الرد (JSON Strict):

### 1. حالة طلب معلومات (Ask):
```json
{
  "action": "ask",
  "question": "سؤال محدد واحد فقط؟",
  "options": ["خيار 1", "خيار 2"]
}
```

### 2. حالة البحث والحساب (Search):
```json
{
  "action": "search",
  "search_terms": ["keywords"],
  "element_type": "type",
  "work_stage": "stage",
  "quantity": 100,
  "unit": "m2"
}
```

## أمثلة للتصحيح الذاتي:

❌ **خطأ (سيناريو المستخدم):**
- مستخدم: "محارة 3 طبقات"
- مساعد: "على أي سطح؟"
- مستخدم: "مباني"
- مساعد: "ما نوع المباني؟ قواعد/أعمدة؟" (خطأ غبي!)

✅ **صحيح:**
- مستخدم: "مباني"
- مساعد: (يفهم أنها Masonry Wall Plastering)
  `{"action": "search", "search_terms": ["plaster", "masonry", "3 coats"], "element_type": "finish", "work_stage": "all"}`

### مثال خرسانة:
- مستخدم: "لبشة"
- مساعد: "ما المرحلة؟"
- مستخدم: "نجارة"
- مساعد: (يفهم أنها Raft Formwork)
  `{"action": "search", "search_terms": ["raft", "formwork"], "element_type": "foundation", "work_stage": "formwork"}`

## 📊 قاعدة البيانات المحسنة (V1.2):
الآن لديك بيانات أغنى لكل بند CSI، استخدمها لتقديم معلومات أفضل:

1. **typical_activities**: قائمة الأنشطة النموذجية لكل بند (Formwork, Reinforcing, Casting, etc.)
   - اعرضها للمستخدم عند تحديد البند
   
2. **implementation_notes**: ملاحظات تنفيذية مهمة (متطلبات اختبار، احتياطات)
   - اذكرها كنصيحة إضافية للمستخدم

3. **default_depth_mm**: السماكة/العمق الافتراضي
   - استخدمها كقيمة مقترحة إذا لم يحددها المستخدم

### مثال رد محسّن:
```json
{
  "action": "search",
  "search_terms": ["raft", "reinforced"],
  "element_type": "foundation",
  "work_stage": "all",
  "enhanced_info": {
    "activities": ["Mesh reinforcement", "Top/bottom mats", "Staged casting", "Curing"],
    "notes": "Heavy reinforcement. Control shrinkage and concrete feed.",
    "suggested_depth": "400-800 mm"
  }
}
```
"""

CSI_AI_SYSTEM_PROMPT_EN = """You are an intelligent assistant specialized in construction and building works. You have a CSI MasterFormat database containing:
- Division 03: Concrete works (footings, columns, beams, slabs)
- Division 07: Waterproofing and thermal insulation
- Division 09: Finishes (plastering, tiles, painting)

## Your Role:
1. Understand user queries (Arabic or English)
2. Identify the type of work required
3. Ask for any missing information for accuracy
4. Search the database and provide accurate results

## Information needed for calculation:
- Type of work (plastering, concrete, tiles, etc.)
- Quantity and unit (m², m³, ton)
- Additional details depending on work type

## Important Rules:
1. If the query is unclear, ask ONE specific question
2. Don't assume - always ask
3. Use emojis to make responses friendly
4. Respond in the same language as the user

## Response Format:
If information is sufficient for search, respond with JSON:
```json
{
  "action": "search",
  "search_terms": ["term1", "term2"],
  "element_type": "footing|column|beam|slab|plaster|tiles|etc",
  "work_stage": "formwork|reinforcement|casting|all|null",
  "quantity": number or null,
  "unit": "m2|m3|ton|null"
}
```

If you need additional information, respond with JSON:
```json
{
  "action": "ask",
  "question": "The clarifying question",
  "options": ["option1", "option2"] // optional
}
```
"""


def get_csi_context(limit: int = 20) -> str:
    """Get sample CSI items for context."""
    if not os.path.exists(DB_PATH):
        return "Database not available."
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Get diverse samples from different divisions
    samples = []
    
    # Concrete items
    rows = conn.execute(
        "SELECT full_code, description, unit, daily_output FROM csi_items "
        "WHERE full_code LIKE '03%' LIMIT 5"
    ).fetchall()
    samples.extend([dict(r) for r in rows])
    
    # Plastering items
    rows = conn.execute(
        "SELECT full_code, description, unit, daily_output FROM csi_items "
        "WHERE full_code LIKE '092%' LIMIT 5"
    ).fetchall()
    samples.extend([dict(r) for r in rows])
    
    # Other finishing items
    rows = conn.execute(
        "SELECT full_code, description, unit, daily_output FROM csi_items "
        "WHERE full_code LIKE '09%' AND full_code NOT LIKE '092%' LIMIT 5"
    ).fetchall()
    samples.extend([dict(r) for r in rows])
    
    conn.close()
    
    context = "## Available CSI Items (samples):\n"
    for item in samples:
        context += f"- {item['full_code']}: {item['description']} ({item['unit']}, {item['daily_output']}/day)\n"
    
    return context


def preprocess_query_with_csi(query: str, lang: str = 'ar') -> Dict[str, Any]:
    """
    Preprocess user query using CSI Lookup Service.
    Returns enriched context with CSI division info and suggestions.
    
    Args:
        query: User's natural language query
        lang: Language ('ar' or 'en')
        
    Returns:
        Dictionary with CSI matches and query analysis
    """
    if not CSI_LOOKUP_AVAILABLE:
        return {"csi_matches": [], "has_matches": False}
    
    try:
        service = get_csi_lookup()
        result = service.smart_search(query, lang=lang, min_confidence=60.0)
        
        matches = result.get('matches', [])
        
        return {
            "csi_matches": matches,
            "has_matches": len(matches) > 0,
            "query_quantity": result.get('query_quantity'),
            "clean_query": result.get('clean_query'),
            "best_match": matches[0] if matches else None
        }
    except Exception as e:
        print(f"[ERROR] CSI Lookup failed: {e}")
        return {"csi_matches": [], "has_matches": False}


def search_database(search_terms: List[str], element_type: str = None, 
                   work_stage: str = None, limit: int = 10) -> List[Dict]:
    """Search CSI database with intelligent matching."""
    if not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Build conditions
    conditions = []
    
    for term in search_terms:
        conditions.append(f"description LIKE '%{term}%'")
    
    # Add work stage filter
    if work_stage == "formwork":
        conditions.append("full_code LIKE '031%'")
    elif work_stage == "reinforcement":
        conditions.append("full_code LIKE '032%'")
    elif work_stage == "casting":
        conditions.append("full_code LIKE '033%'")
    
    # Add element type filter
    if element_type == "plaster":
        conditions.append("full_code LIKE '092%'")
    elif element_type == "tiles":
        conditions.append("full_code LIKE '093%'")
    
    where_clause = " OR ".join(conditions[:3]) if conditions else "1=1"
    if len(conditions) > 3:
        # Add mandatory conditions with AND
        mandatory = " AND ".join(conditions[3:])
        where_clause = f"({where_clause}) AND ({mandatory})"
    
    sql = f"""
        SELECT full_code, description, unit, daily_output, man_hours, 
               equip_hours, crew_structure
        FROM csi_items 
        WHERE {where_clause}
        LIMIT {limit}
    """
    
    try:
        rows = conn.execute(sql).fetchall()
        results = [dict(r) for r in rows]
    except Exception as e:
        results = []
    finally:
        conn.close()
    
    return results


def calculate_productivity(item: Dict, quantity: float, num_crews: int = 1) -> Dict:
    """Calculate duration and productivity for an item."""
    daily_output = item.get('daily_output', 1) or 1
    man_hours = item.get('man_hours', 0) or 0
    
    # Duration in days
    duration_days = quantity / (daily_output * num_crews)
    
    # Total man-hours
    total_man_hours = (quantity / daily_output) * man_hours
    
    return {
        "item_code": item.get('full_code'),
        "item_description": item.get('description'),
        "unit": item.get('unit'),
        "quantity": quantity,
        "daily_output": daily_output,
        "num_crews": num_crews,
        "duration_days": round(duration_days, 2),
        "total_man_hours": round(total_man_hours, 2),
        "crew_structure": item.get('crew_structure')
    }


def process_ai_response(ai_response: str, lang: str = "ar") -> Dict[str, Any]:
    """Process AI response and take appropriate action."""
    # Try to extract JSON from response
    try:
        # Find JSON in response
        json_start = ai_response.find('{')
        json_end = ai_response.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = ai_response[json_start:json_end]
            data = json.loads(json_str)
            return data
    except json.JSONDecodeError:
        pass
    
    # If no JSON found, treat as direct text response
    return {
        "action": "respond",
        "message": ai_response
    }


def format_search_results(results: List[Dict], lang: str = "ar") -> str:
    """Format search results as readable text."""
    if not results:
        if lang == "ar":
            return "❌ لم أجد نتائج مطابقة. جرب البحث بكلمات أخرى."
        return "❌ No matching results found. Try different search terms."
    
    if lang == "ar":
        text = f"📋 **وجدت {len(results)} بند مطابق:**\n\n"
    else:
        text = f"📋 **Found {len(results)} matching items:**\n\n"
    
    for i, item in enumerate(results[:5], 1):
        code = item.get('full_code', 'N/A')
        desc = item.get('description', 'N/A')[:60]
        unit = item.get('unit', 'N/A')
        output = item.get('daily_output', 'N/A')
        
        text += f"**{i}. {code}**\n"
        text += f"   {desc}\n"
        text += f"   📏 {unit} | ⚡ {output}/day\n\n"
    
    if lang == "ar":
        text += "\n💡 **اختر بند وأخبرني بالكمية لحساب المدة الزمنية.**"
    else:
        text += "\n💡 **Select an item and tell me the quantity to calculate duration.**"
    
    return text
