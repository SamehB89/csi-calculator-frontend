from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import requests
import json

app = Flask(__name__)
CORS(app)

import math

# ===== Groq AI Configuration =====
# Free tier: 14,400 requests/day (vs Gemini's 50!)
# Faster, more reliable, and much higher quota
# Get your free API key from: https://console.groq.com/keys

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("[WARNING] groq not installed. Run: pip install groq")

# Groq API Key (much better than Gemini!)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Configure Groq client
if GROQ_AVAILABLE and GROQ_API_KEY:
    GROQ_CLIENT = Groq(api_key=GROQ_API_KEY)
    AI_MODEL_NAME = "llama-3.3-70b-versatile"  # Best free model
    print(f"[OK] ⚡ Groq AI configured! Model: {AI_MODEL_NAME}")
    print(f"[INFO] 🚀 Daily quota: 14,400 requests (vs Gemini's 50)")
elif GROQ_AVAILABLE and not GROQ_API_KEY:
    GROQ_CLIENT = None
    print("[WARNING] ⚠️ GROQ_API_KEY not set! AI features disabled.")
    print("[INFO] Get free key from: https://console.groq.com/keys")
else:
    GROQ_CLIENT = None

# User-provided Rates & Defaults
RATES = {
    "ar": {
        "carpentry_m2_per_day_per_carpenter": 15,
        "rebar_ton_per_day_per_steel_fixer": 0.8,
        "concrete_m3_per_hour_pump": 20,
        "crew_defaults": {
            "excavation": "حفار + 2 عمّال",
            "formwork": "4 نجّارين + 2 عمّال",
            "rebar": "3 حدادين + 2 عمّال",
            "pour": "فريق صب 6 عمّال",
            "curing": "2 عمّال"
        },
        "equipment_defaults": {
            "excavation": "حفّار + قلابات",
            "formwork": "معدات يدويّة",
            "rebar": "معدات حدادة",
            "pour": "خلاطة + مضخة",
            "curing": "رشّ مياه"
        }
    },
    "en": {
        "carpentry_m2_per_day_per_carpenter": 15,
        "rebar_ton_per_day_per_steel_fixer": 0.8,
        "concrete_m3_per_hour_pump": 20,
        "crew_defaults": {
            "excavation": "Excavator + 2 laborers",
            "formwork": "4 carpenters + 2 laborers",
            "rebar": "3 steel fixers + 2 laborers",
            "pour": "Pouring crew 6 laborers",
            "curing": "2 laborers"
        },
        "equipment_defaults": {
            "excavation": "Excavator + trucks",
            "formwork": "Hand tools",
            "rebar": "Rebar tools",
            "pour": "Mixer + pump",
            "curing": "Water spray"
        }
    }
}

def parse_query(q):
    """Parse user query to extract quantity, unit, and scope/element type"""
    q = q.lower()
    qty = None
    unit = None
    
    # Quantity parsing
    for token in q.replace("م٣","م3").replace("cubic","m3").replace("cum","m3").split():
        if "m3" in token or "م3" in token:
            try:
                qty = float(''.join([c for c in token if c.isdigit() or c=='.']))
                unit = "m3"
            except:
                pass
    
    # Fallback: search for any number
    if qty is None:
        nums = ''.join([c if c.isdigit() or c=='.' else ' ' for c in q]).split()
        if nums:
            try:
                qty = float(nums[0])
            except:
                qty = None

    # Detect scope/element type from keywords
    # Order matters - more specific matches first
    
    # Slabs
    if any(k in q for k in ["slab", "slabs", "بلاطة", "بلاطات", "سقف", "أسقف"]):
        scope = "slabs"
    # Beams
    elif any(k in q for k in ["beam", "beams", "كمرة", "كمرات", "جسر", "جسور"]):
        scope = "beams"
    # Columns
    elif any(k in q for k in ["column", "columns", "عمود", "أعمدة", "عامود"]):
        scope = "columns"
    # Piles
    elif any(k in q for k in ["pile", "piles", "خازوق", "خوازيق"]):
        scope = "piles"
        # For piles, interpret qty as number of piles
        unit = "piles"
    # Strip foundations
    elif any(k in q for k in ["strip", "continuous", "شريطي", "شريطية", "مستمر", "سملات"]):
        scope = "strip_foundation"
    # Raft foundations
    elif any(k in q for k in ["raft", "mat", "labsha", "لبشة", "حصيرية"]):
        scope = "raft_foundation"
    # Isolated foundations (default foundation type)
    elif any(k in q for k in ["foundation", "foundations", "أساسات", "قواعد", "isolated", "منفصلة", "منفصل"]):
        scope = "isolated_foundations"
    # Generic fallback
    else:
        scope = "unknown"

    return qty, unit or "m3", scope

def plan_isolated_foundations(qty_m3, lang):
    L = RATES[lang]
    rows = []

    # Assumptions (Isolated: High Formwork Ratio)
    formwork_area = qty_m3 * 1.2
    rebar_ton = qty_m3 * 0.08
    
    carp_rate = L["carpentry_m2_per_day_per_carpenter"] * 4
    rebar_rate = L["rebar_ton_per_day_per_steel_fixer"] * 3
    pump_rate_m3_per_day = L["concrete_m3_per_hour_pump"] * 6

    # Excavation
    exc_days = math.ceil(qty_m3 / 40.0)
    rows.append({
        "task": "حفر" if lang == "ar" else "Excavation",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["excavation"],
        "equipment": L["equipment_defaults"]["excavation"],
        "duration": f"{exc_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Formwork
    form_days = math.ceil(formwork_area / carp_rate)
    rows.append({
        "task": "نجارة شدّات" if lang == "ar" else "Formwork",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": L["crew_defaults"]["formwork"],
        "equipment": L["equipment_defaults"]["formwork"],
        "duration": f"{form_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Rebar
    rebar_days = math.ceil(rebar_ton / rebar_rate)
    rows.append({
        "task": "حدادة مسلّحة" if lang == "ar" else "Rebar",
        "qty": f"{rebar_ton:.2f}",
        "unit": "طن" if lang == "ar" else "ton",
        "crew": L["crew_defaults"]["rebar"],
        "equipment": L["equipment_defaults"]["rebar"],
        "duration": f"{rebar_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Pouring
    pour_days = math.ceil(qty_m3 / pump_rate_m3_per_day)
    rows.append({
        "task": "صب خرسانة" if lang == "ar" else "Concrete Pour",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["pour"],
        "equipment": L["equipment_defaults"]["pour"],
        "duration": f"{pour_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Curing
    cure_days = 7
    rows.append({
        "task": "معالجة خرسانة" if lang == "ar" else "Curing",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["curing"],
        "equipment": L["equipment_defaults"]["curing"],
        "duration": f"{cure_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Overall text
    if lang == "ar":
        text = (
            "تم توليد خطة للأساسات المنفصلة:\n"
            f"- الكمية: {qty_m3} م³\n"
            f"- تقدير شدّات: {formwork_area:.1f} م²\n"
            f"- تقدير حديد: {rebar_ton:.2f} طن\n"
            f"- المدة التقريبية: {exc_days + form_days + rebar_days + pour_days + cure_days} يوم"
        )
        notes = "معدلات تقريبية للأساسات المنفصلة."
    else:
        text = (
            "Generated plan for Isolated Foundations:\n"
            f"- Quantity: {qty_m3} m3\n"
            f"- Formwork: {formwork_area:.1f} m2\n"
            f"- Rebar: {rebar_ton:.2f} ton\n"
            f"- Approx Duration: {exc_days + form_days + rebar_days + pour_days + cure_days} days"
        )
        notes = "Approximate rates for isolated footings."

    return {
        "text": text,
        "table": { "rows": rows },
        "notes": notes
    }

def plan_raft_foundation(qty_m3, lang):
    L = RATES[lang]
    rows = []

    # Assumptions (Raft: Lower Formwork Ratio, Higher Rebar)
    # Raft is mostly volume, less side area.
    formwork_area = qty_m3 * 0.4  # significantly less per m3 than isolated
    rebar_ton = qty_m3 * 0.10     # often heavier reinforcement (100kg/m3)
    
    carp_rate = L["carpentry_m2_per_day_per_carpenter"] * 4
    rebar_rate = L["rebar_ton_per_day_per_steel_fixer"] * 3
    pump_rate_m3_per_day = L["concrete_m3_per_hour_pump"] * 8  # Long pour days for rafts

    # Excavation (Mass excavation)
    exc_days = math.ceil(qty_m3 / 80.0) # Faster (larger equipment)
    rows.append({
        "task": "حفر لبشة" if lang == "ar" else "Mass Excavation",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["excavation"],
        "equipment": L["equipment_defaults"]["excavation"],
        "duration": f"{exc_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Formwork
    form_days = math.ceil(formwork_area / carp_rate)
    rows.append({
        "task": "نجارة جوانب اللبشة" if lang == "ar" else "Raft Side Formwork",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": L["crew_defaults"]["formwork"],
        "equipment": L["equipment_defaults"]["formwork"],
        "duration": f"{form_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Rebar (Takes longer usually)
    rebar_days = math.ceil(rebar_ton / rebar_rate)
    rows.append({
        "task": "حدادة اللبشة" if lang == "ar" else "Raft Rebar",
        "qty": f"{rebar_ton:.2f}",
        "unit": "طن" if lang == "ar" else "ton",
        "crew": L["crew_defaults"]["rebar"],
        "equipment": L["equipment_defaults"]["rebar"],
        "duration": f"{rebar_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Pouring (Massive pour)
    pour_days = math.ceil(qty_m3 / pump_rate_m3_per_day)
    rows.append({
        "task": "صب خرسانة اللبشة" if lang == "ar" else "Raft Concrete Pour",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": "2x " + L["crew_defaults"]["pour"], # Double crew for raft
        "equipment": "2x " + L["equipment_defaults"]["pour"],
        "duration": f"{pour_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Curing
    cure_days = 14 # Longer curing for mass concrete
    rows.append({
        "task": "معالجة (غمْر بالمياه)" if lang == "ar" else "Curing (Ponding)",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["curing"],
        "equipment": L["equipment_defaults"]["curing"],
        "duration": f"{cure_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Overall text
    if lang == "ar":
        text = (
            "تم توليد خطة للبشة الخرسانية (Raft):\n"
            f"- الكمية: {qty_m3} م³\n"
            f"- مساحة الجوانب التقديرية: {formwork_area:.1f} م²\n"
            f"- حديد التسليح التقديري (100كجم/م³): {rebar_ton:.2f} طن\n"
            f"- المدة الزمنية: {exc_days + form_days + rebar_days + pour_days + cure_days} يوم"
        )
        notes = "تم افتراض صب اللبشة باستخدام مضختين وفريقين لضمان الاستمرارية."
    else:
        text = (
            "Generated plan for Raft Foundation (Mat):\n"
            f"- Quantity: {qty_m3} m3\n"
            f"- Side Formwork: {formwork_area:.1f} m2\n"
            f"- Rebar (approx 100kg/m3): {rebar_ton:.2f} ton\n"
            f"- Duration: {exc_days + form_days + rebar_days + pour_days + cure_days} days"
        )
        notes = "Assumed usage of 2 concrete pumps and double crew for massive pour continuity."

    return {
        "text": text,
        "table": { "rows": rows },
        "notes": notes
    }

def plan_strip_foundation(qty_m3, lang):
    """Plan for strip/continuous foundations"""
    L = RATES[lang]
    rows = []

    # Strip foundations have linear formwork
    formwork_area = qty_m3 * 0.9  # Less than isolated, more than raft
    rebar_ton = qty_m3 * 0.07    # 70 kg/m3 typical
    
    carp_rate = L["carpentry_m2_per_day_per_carpenter"] * 4
    rebar_rate = L["rebar_ton_per_day_per_steel_fixer"] * 3
    pump_rate_m3_per_day = L["concrete_m3_per_hour_pump"] * 6

    # Excavation (Linear trenches)
    exc_days = math.ceil(qty_m3 / 50.0)
    rows.append({
        "task": "حفر خنادق" if lang == "ar" else "Trench Excavation",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["excavation"],
        "equipment": L["equipment_defaults"]["excavation"],
        "duration": f"{exc_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Formwork
    form_days = math.ceil(formwork_area / carp_rate)
    rows.append({
        "task": "نجارة شدّات شريطية" if lang == "ar" else "Strip Formwork",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": L["crew_defaults"]["formwork"],
        "equipment": L["equipment_defaults"]["formwork"],
        "duration": f"{form_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Rebar
    rebar_days = math.ceil(rebar_ton / rebar_rate)
    rows.append({
        "task": "حدادة مسلّحة" if lang == "ar" else "Rebar Installation",
        "qty": f"{rebar_ton:.2f}",
        "unit": "طن" if lang == "ar" else "ton",
        "crew": L["crew_defaults"]["rebar"],
        "equipment": L["equipment_defaults"]["rebar"],
        "duration": f"{rebar_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Pouring
    pour_days = math.ceil(qty_m3 / pump_rate_m3_per_day)
    rows.append({
        "task": "صب خرسانة" if lang == "ar" else "Concrete Pour",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["pour"],
        "equipment": L["equipment_defaults"]["pour"],
        "duration": f"{pour_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Curing
    cure_days = 7
    rows.append({
        "task": "معالجة خرسانة" if lang == "ar" else "Curing",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["curing"],
        "equipment": L["equipment_defaults"]["curing"],
        "duration": f"{cure_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    total_days = exc_days + form_days + rebar_days + pour_days + cure_days
    
    if lang == "ar":
        text = (
            "تم توليد خطة للأساسات الشريطية:\n"
            f"- الكمية: {qty_m3} م³\n"
            f"- تقدير شدّات: {formwork_area:.1f} م²\n"
            f"- تقدير حديد: {rebar_ton:.2f} طن\n"
            f"- المدة التقريبية: {total_days} يوم"
        )
        notes = "معدلات تقريبية للأساسات الشريطية المستمرة."
    else:
        text = (
            "Generated plan for Strip Foundations:\n"
            f"- Quantity: {qty_m3} m3\n"
            f"- Formwork: {formwork_area:.1f} m2\n"
            f"- Rebar: {rebar_ton:.2f} ton\n"
            f"- Approx Duration: {total_days} days"
        )
        notes = "Approximate rates for continuous strip footings."

    return {
        "text": text,
        "table": { "rows": rows },
        "notes": notes
    }

def plan_pile_foundation(qty_piles, lang):
    """Plan for pile foundation (qty = number of piles)"""
    L = RATES[lang]
    rows = []

    # Pile assumptions: 10m deep, 0.5m diameter average
    avg_pile_volume = 2.0  # m3 per pile
    total_concrete = qty_piles * avg_pile_volume
    rebar_ton = qty_piles * 0.15  # 150kg per pile
    
    # Drilling rate: 3 piles per day
    drill_days = math.ceil(qty_piles / 3)
    rows.append({
        "task": "حفر الخوازيق" if lang == "ar" else "Pile Drilling",
        "qty": f"{qty_piles}",
        "unit": "خازوق" if lang == "ar" else "pile",
        "crew": "2 مشغّلين + 3 عمّال" if lang == "ar" else "2 operators + 3 laborers",
        "equipment": "ماكينة حفر خوازيق" if lang == "ar" else "Pile drilling rig",
        "duration": f"{drill_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Rebar cage installation
    rebar_days = math.ceil(qty_piles / 6)  # 6 cages per day
    rows.append({
        "task": "تركيب أقفاص الحديد" if lang == "ar" else "Rebar Cage Installation",
        "qty": f"{qty_piles}",
        "unit": "قفص" if lang == "ar" else "cage",
        "crew": L["crew_defaults"]["rebar"],
        "equipment": "رافعة + معدات حدادة" if lang == "ar" else "Crane + rebar tools",
        "duration": f"{rebar_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Concrete pouring (tremie method)
    pour_days = math.ceil(qty_piles / 8)  # 8 piles per day
    rows.append({
        "task": "صب خرسانة بالتريمي" if lang == "ar" else "Tremie Concrete Pour",
        "qty": f"{total_concrete:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["pour"],
        "equipment": "مضخة + ترمي" if lang == "ar" else "Pump + tremie pipe",
        "duration": f"{pour_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Pile cap preparation
    cap_days = math.ceil(qty_piles / 10)
    rows.append({
        "task": "تكسير رؤوس الخوازيق" if lang == "ar" else "Pile Head Breaking",
        "qty": f"{qty_piles}",
        "unit": "خازوق" if lang == "ar" else "pile",
        "crew": "4 عمّال + مشرف" if lang == "ar" else "4 laborers + supervisor",
        "equipment": "هيلتي + كمبريسور" if lang == "ar" else "Jack hammer + compressor",
        "duration": f"{cap_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    total_days = drill_days + rebar_days + pour_days + cap_days
    
    if lang == "ar":
        text = (
            "تم توليد خطة لأعمال الخوازيق:\n"
            f"- عدد الخوازيق: {qty_piles}\n"
            f"- حجم الخرسانة: {total_concrete:.1f} م³\n"
            f"- حديد التسليح: {rebar_ton:.2f} طن\n"
            f"- المدة التقريبية: {total_days} يوم"
        )
        notes = "تفترض الخطة خوازيق بقطر 50سم وعمق 10م."
    else:
        text = (
            "Generated plan for Pile Foundation:\n"
            f"- Number of Piles: {qty_piles}\n"
            f"- Concrete Volume: {total_concrete:.1f} m3\n"
            f"- Rebar: {rebar_ton:.2f} ton\n"
            f"- Duration: {total_days} days"
        )
        notes = "Plan assumes 500mm diameter piles at 10m depth."

    return {
        "text": text,
        "table": { "rows": rows },
        "notes": notes
    }

def plan_columns(qty_m3, lang):
    """Plan for reinforced concrete columns"""
    L = RATES[lang]
    rows = []

    # Columns have high formwork ratio (all sides)
    formwork_area = qty_m3 * 2.5  # High ratio
    rebar_ton = qty_m3 * 0.15    # 150 kg/m3 (heavy reinforcement)
    
    carp_rate = L["carpentry_m2_per_day_per_carpenter"] * 3  # Slower for columns
    rebar_rate = L["rebar_ton_per_day_per_steel_fixer"] * 2
    pump_rate_m3_per_day = L["concrete_m3_per_hour_pump"] * 4  # Slower for columns

    # Formwork
    form_days = math.ceil(formwork_area / carp_rate)
    rows.append({
        "task": "نجارة شدّات أعمدة" if lang == "ar" else "Column Formwork",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": L["crew_defaults"]["formwork"],
        "equipment": L["equipment_defaults"]["formwork"],
        "duration": f"{form_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Rebar
    rebar_days = math.ceil(rebar_ton / rebar_rate)
    rows.append({
        "task": "حدادة أعمدة" if lang == "ar" else "Column Rebar",
        "qty": f"{rebar_ton:.2f}",
        "unit": "طن" if lang == "ar" else "ton",
        "crew": L["crew_defaults"]["rebar"],
        "equipment": L["equipment_defaults"]["rebar"],
        "duration": f"{rebar_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Pouring
    pour_days = math.ceil(qty_m3 / pump_rate_m3_per_day)
    rows.append({
        "task": "صب خرسانة أعمدة" if lang == "ar" else "Column Concrete Pour",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["pour"],
        "equipment": L["equipment_defaults"]["pour"],
        "duration": f"{pour_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Stripping
    strip_days = math.ceil(formwork_area / (carp_rate * 1.5))
    rows.append({
        "task": "فك الشدّات" if lang == "ar" else "Form Stripping",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": L["crew_defaults"]["formwork"],
        "equipment": L["equipment_defaults"]["formwork"],
        "duration": f"{strip_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    total_days = form_days + rebar_days + pour_days + strip_days
    
    if lang == "ar":
        text = (
            "تم توليد خطة للأعمدة الخرسانية:\n"
            f"- الكمية: {qty_m3} م³\n"
            f"- مساحة الشدّات: {formwork_area:.1f} م²\n"
            f"- حديد التسليح: {rebar_ton:.2f} طن\n"
            f"- المدة التقريبية: {total_days} يوم"
        )
        notes = "معدلات تقريبية للأعمدة (تسليح 150 كجم/م³)."
    else:
        text = (
            "Generated plan for RC Columns:\n"
            f"- Quantity: {qty_m3} m3\n"
            f"- Formwork: {formwork_area:.1f} m2\n"
            f"- Rebar (150kg/m3): {rebar_ton:.2f} ton\n"
            f"- Duration: {total_days} days"
        )
        notes = "Rates for typical RC columns with heavy reinforcement."

    return {
        "text": text,
        "table": { "rows": rows },
        "notes": notes
    }

def plan_beams(qty_m3, lang):
    """Plan for reinforced concrete beams"""
    L = RATES[lang]
    rows = []

    # Beams formwork includes bottom and sides
    formwork_area = qty_m3 * 2.0
    rebar_ton = qty_m3 * 0.12    # 120 kg/m3
    
    carp_rate = L["carpentry_m2_per_day_per_carpenter"] * 3.5
    rebar_rate = L["rebar_ton_per_day_per_steel_fixer"] * 2.5
    pump_rate_m3_per_day = L["concrete_m3_per_hour_pump"] * 5

    # Formwork
    form_days = math.ceil(formwork_area / carp_rate)
    rows.append({
        "task": "نجارة شدّات كمرات" if lang == "ar" else "Beam Formwork",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": L["crew_defaults"]["formwork"],
        "equipment": L["equipment_defaults"]["formwork"],
        "duration": f"{form_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Rebar
    rebar_days = math.ceil(rebar_ton / rebar_rate)
    rows.append({
        "task": "حدادة كمرات" if lang == "ar" else "Beam Rebar",
        "qty": f"{rebar_ton:.2f}",
        "unit": "طن" if lang == "ar" else "ton",
        "crew": L["crew_defaults"]["rebar"],
        "equipment": L["equipment_defaults"]["rebar"],
        "duration": f"{rebar_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Pouring
    pour_days = math.ceil(qty_m3 / pump_rate_m3_per_day)
    rows.append({
        "task": "صب خرسانة كمرات" if lang == "ar" else "Beam Concrete Pour",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["pour"],
        "equipment": L["equipment_defaults"]["pour"],
        "duration": f"{pour_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Curing + Stripping (after 14 days)
    cure_days = 14
    rows.append({
        "task": "معالجة وفك شدّات" if lang == "ar" else "Curing & Stripping",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["curing"],
        "equipment": L["equipment_defaults"]["curing"],
        "duration": f"{cure_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    total_days = form_days + rebar_days + pour_days + cure_days
    
    if lang == "ar":
        text = (
            "تم توليد خطة للكمرات الخرسانية:\n"
            f"- الكمية: {qty_m3} م³\n"
            f"- مساحة الشدّات: {formwork_area:.1f} م²\n"
            f"- حديد التسليح: {rebar_ton:.2f} طن\n"
            f"- المدة التقريبية: {total_days} يوم"
        )
        notes = "معدلات تقريبية للكمرات (فك الشدّات بعد 14 يوم)."
    else:
        text = (
            "Generated plan for RC Beams:\n"
            f"- Quantity: {qty_m3} m3\n"
            f"- Formwork: {formwork_area:.1f} m2\n"
            f"- Rebar: {rebar_ton:.2f} ton\n"
            f"- Duration: {total_days} days"
        )
        notes = "Form stripping after 14 days curing period."

    return {
        "text": text,
        "table": { "rows": rows },
        "notes": notes
    }

def plan_slabs(qty_m3, lang):
    """Plan for reinforced concrete slabs"""
    L = RATES[lang]
    rows = []

    # Slabs - large bottom form area, minimal sides
    # Assume 20cm thick slab: 1 m3 = 5 m2
    formwork_area = qty_m3 * 5.0
    rebar_ton = qty_m3 * 0.08    # 80 kg/m3
    
    carp_rate = L["carpentry_m2_per_day_per_carpenter"] * 5  # Faster for slabs
    rebar_rate = L["rebar_ton_per_day_per_steel_fixer"] * 3
    pump_rate_m3_per_day = L["concrete_m3_per_hour_pump"] * 8  # Faster for slabs

    # Formwork + Shoring
    form_days = math.ceil(formwork_area / carp_rate)
    rows.append({
        "task": "نجارة وتدعيم بلاطة" if lang == "ar" else "Slab Formwork & Shoring",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": L["crew_defaults"]["formwork"],
        "equipment": "شدّات + جكات تدعيم" if lang == "ar" else "Forms + shoring jacks",
        "duration": f"{form_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Rebar (mesh + additional)
    rebar_days = math.ceil(rebar_ton / rebar_rate)
    rows.append({
        "task": "حدادة بلاطة" if lang == "ar" else "Slab Rebar",
        "qty": f"{rebar_ton:.2f}",
        "unit": "طن" if lang == "ar" else "ton",
        "crew": L["crew_defaults"]["rebar"],
        "equipment": L["equipment_defaults"]["rebar"],
        "duration": f"{rebar_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # MEP conduits
    mep_days = math.ceil(formwork_area / 200)  # 200 m2 per day
    rows.append({
        "task": "تمديدات كهربائية" if lang == "ar" else "MEP Conduits",
        "qty": f"{formwork_area:.1f}",
        "unit": "م²" if lang == "ar" else "m2",
        "crew": "2 كهربائيين + 2 سباكين" if lang == "ar" else "2 electricians + 2 plumbers",
        "equipment": "معدات يدوية" if lang == "ar" else "Hand tools",
        "duration": f"{mep_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Pouring
    pour_days = math.ceil(qty_m3 / pump_rate_m3_per_day)
    rows.append({
        "task": "صب خرسانة بلاطة" if lang == "ar" else "Slab Concrete Pour",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["pour"],
        "equipment": L["equipment_defaults"]["pour"],
        "duration": f"{pour_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    # Curing + Stripping
    cure_days = 21  # 21 days for slabs
    rows.append({
        "task": "معالجة وفك تدعيم" if lang == "ar" else "Curing & Reshoring",
        "qty": f"{qty_m3:.1f}",
        "unit": "م³" if lang == "ar" else "m3",
        "crew": L["crew_defaults"]["curing"],
        "equipment": L["equipment_defaults"]["curing"],
        "duration": f"{cure_days} { 'يوم' if lang=='ar' else 'day' }"
    })

    total_days = form_days + rebar_days + mep_days + pour_days + cure_days
    
    if lang == "ar":
        text = (
            "تم توليد خطة للبلاطات الخرسانية:\n"
            f"- الكمية: {qty_m3} م³\n"
            f"- مساحة الشدّات: {formwork_area:.1f} م²\n"
            f"- حديد التسليح: {rebar_ton:.2f} طن\n"
            f"- المدة التقريبية: {total_days} يوم"
        )
        notes = "البلاطة المفترضة 20سم سمك. فك التدعيم بعد 21 يوم."
    else:
        text = (
            "Generated plan for RC Slab:\n"
            f"- Quantity: {qty_m3} m3\n"
            f"- Formwork: {formwork_area:.1f} m2\n"
            f"- Rebar: {rebar_ton:.2f} ton\n"
            f"- Duration: {total_days} days"
        )
        notes = "Assumes 200mm thick slab. Reshoring removal after 21 days."

    return {
        "text": text,
        "table": { "rows": rows },
        "notes": notes
    }

OLLAMA_API_URL = "http://localhost:11434/api/chat"
TAGS_API_URL = "http://localhost:11434/api/tags"
DEFAULT_MODEL = "llama3.2" 

# Global variable to cache the working model
CURRENT_MODEL = None

def get_working_model():
    global CURRENT_MODEL
    if CURRENT_MODEL:
        return CURRENT_MODEL
    
    # Try default first
    try:
        # Check if default model exists in tags
        res = requests.get(TAGS_API_URL)
        if res.status_code == 200:
            models = res.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            # 1. Try exact match
            if DEFAULT_MODEL in model_names:
                CURRENT_MODEL = DEFAULT_MODEL
                return DEFAULT_MODEL
            
            # 2. Try partial match (e.g. 'llama3.2:latest' matches 'llama3.2')
            for m in model_names:
                if DEFAULT_MODEL in m:
                    CURRENT_MODEL = m
                    return m
            
            # 3. Fallback to 'llama3' or 'mistral'
            for m in model_names:
                if 'llama3' in m or 'mistral' in m:
                    CURRENT_MODEL = m
                    return m
            
            # 4. Fallback to ANY model that isn't an embedder
            for m in model_names:
                if 'embed' not in m:
                    CURRENT_MODEL = m
                    return m
                    
    except Exception as e:
        print(f"Error checking models: {e}")
    
    return DEFAULT_MODEL # Hope for the best

# Database configuration - supports both local SQLite and PostgreSQL cloud database
from db_config import get_db_connection

# Health check endpoint for Railway
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify deployment"""
    try:
        db_url = os.environ.get('DATABASE_URL', 'Not set')
        db_status = 'PostgreSQL' if db_url != 'Not set' else 'SQLite (local)'
        
        # Test database connection
        db_connected = False
        count = 0
        error_detail = None
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM csi_items")
            result = cursor.fetchone()
            count = result[0] if result else 0
            conn.close()
            db_connected = True
        except Exception as e:
            error_detail = str(e)
            count = 0
        
        response = {
            "status": "healthy" if db_connected else "database_error",
            "database": db_status,
            "database_connected": db_connected,
            "items_count": count,
            "environment": "production" if db_url != 'Not set' else "development"
        }
        
        if error_detail:
            response["error"] = error_detail
            
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/divisions', methods=['GET'])
def get_divisions():
    try:
        conn = get_db_connection()
        # Get distinct Main Divisions - ORDER BY CAST for proper numeric sorting (SQLite compatible)
        divisions = conn.execute(
            "SELECT DISTINCT main_div_code, main_div_name FROM csi_items "
            "WHERE main_div_code IS NOT NULL AND main_div_code != '' "
            "ORDER BY CAST(main_div_code AS INTEGER)"
        ).fetchall()
        conn.close()
        return jsonify([{'code': row['main_div_code'], 'name': row['main_div_name']} for row in divisions])
    except Exception as e:
        print(f"Error in get_divisions: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/subdivisions1', methods=['GET'])
def get_subdivisions1():
    main_code = request.args.get('main_code')
    if not main_code:
        return jsonify([])
    
    try:
        conn = get_db_connection()
        # GROUP BY name to avoid duplicates, MIN(code) to get representative code
        subs = conn.execute(
            "SELECT MIN(sub_div1_code) as sub_div1_code, sub_div1_name FROM csi_items "
            "WHERE main_div_code = ? AND sub_div1_code IS NOT NULL AND sub_div1_code != '' "
            "GROUP BY sub_div1_name "
            "ORDER BY CAST(MIN(sub_div1_code) AS INTEGER)",
            (main_code,)
        ).fetchall()
        conn.close()
        return jsonify([{'code': row['sub_div1_code'], 'name': row['sub_div1_name']} for row in subs])
    except Exception as e:
        print(f"Error in get_subdivisions1: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/subdivisions2', methods=['GET'])
def get_subdivisions2():
    main_code = request.args.get('main_code')
    sub1_code = request.args.get('sub1_code')
    if not sub1_code:
        return jsonify([])
    
    try:
        conn = get_db_connection()
        # GROUP BY name to avoid duplicates, MIN(code) to get representative code
        if main_code:
            subs = conn.execute(
                "SELECT MIN(sub_div2_code) as sub_div2_code, sub_div2_name FROM csi_items "
                "WHERE main_div_code = ? AND sub_div1_code = ? "
                "AND sub_div2_code IS NOT NULL AND sub_div2_code != '' "
                "GROUP BY sub_div2_name "
                "ORDER BY CAST(MIN(sub_div2_code) AS INTEGER)",
                (main_code, sub1_code)
            ).fetchall()
        else:
            # Fallback for backward compatibility
            subs = conn.execute(
                "SELECT MIN(sub_div2_code) as sub_div2_code, sub_div2_name FROM csi_items "
                "WHERE sub_div1_code = ? "
                "AND sub_div2_code IS NOT NULL AND sub_div2_code != '' "
                "GROUP BY sub_div2_name "
                "ORDER BY CAST(MIN(sub_div2_code) AS INTEGER)",
                (sub1_code,)
            ).fetchall()
            
        conn.close()
        return jsonify([{'code': row['sub_div2_code'], 'name': row['sub_div2_name']} for row in subs])
    except Exception as e:
        print(f"Error in get_subdivisions2: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/items', methods=['GET'])
def get_items():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 50)
    main_code = request.args.get('main_code')
    sub1_code = request.args.get('sub1_code')
    sub2_code = request.args.get('sub2_code')
    
    sql = 'SELECT * FROM csi_items WHERE 1=1'
    params = []
    
    if main_code:
        sql += ' AND main_div_code = ?'
        params.append(main_code)
    if sub1_code:
        sql += ' AND sub_div1_code = ?'
        params.append(sub1_code)
    if sub2_code:
        sql += ' AND sub_div2_code = ?'
        params.append(sub2_code)
        
    if query:
        sql += ' AND (full_code LIKE ? OR description LIKE ?)'
        params.append(f'%{query}%')
        params.append(f'%{query}%')
        
    sql += f' LIMIT {limit}'
    
    conn = get_db_connection()
    items = conn.execute(sql, params).fetchall()
    conn.close()
    
    return jsonify({
        'items': [dict(row) for row in items],
        'count': len(items)
    })

@app.route('/api/calculate-crew', methods=['POST'])
def calculate_crew():
    """
    Calculate crew requirements based on item code and quantity
    Input JSON: {
        "item_code": "033 172-2950",
        "quantity": 100,
        "hours_per_day": 8,
        "number_of_crews": 2
    }
    """
    data = request.json
    item_code = data.get('item_code')
    quantity = float(data.get('quantity', 0))
    hours_per_day = float(data.get('hours_per_day', 8))
    number_of_crews = int(data.get('number_of_crews', 1))
    
    if not item_code or quantity <= 0:
        return jsonify({'error': 'Invalid input'}), 400
    
    if number_of_crews < 1:
        return jsonify({'error': 'Number of crews must be at least 1'}), 400
    
    # Get item from database
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM csi_items WHERE full_code = ?', (item_code,)).fetchone()
    conn.close()
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    # Extract data
    daily_output = item['daily_output']
    man_hours = item['man_hours']
    equip_hours = item['equip_hours']
    
    if not daily_output or not man_hours:
        return jsonify({'error': 'Item does not have productivity data'}), 400
    
    # Calculate adjusted daily output based on number of crews
    adjusted_daily_output = daily_output * number_of_crews
    
    # Calculate total days (reduced by number of crews)
    total_days = quantity / adjusted_daily_output
    total_hours = total_days * hours_per_day
    
    # Calculate total man hours (remains the same - total work doesn't change)
    total_man_hours = quantity * man_hours
    total_equip_hours = quantity * (equip_hours or 0)
    
    # Parse crew structure
    crew_members = []
    for i in range(1, 13):  # Up to 12 crew members
        crew_num = item[f'crew_num_{i}']
        crew_desc = item[f'crew_desc_{i}']
        
        if crew_num and crew_desc:
            try:
                count_per_crew = float(crew_num)
                total_count = count_per_crew * number_of_crews  # Multiply by number of crews
                crew_members.append({
                    'position': crew_desc,
                    'count': total_count,  # Total across all crews
                    'count_per_crew': count_per_crew,  # Count for single crew
                    'total_hours': total_hours * count_per_crew,
                    'type': 'equipment' if any(word in crew_desc.lower() for word in ['crane', 'truck', 'pump', 'vibrator', 'tool', 'dozer', 'loader', 'excavator', 'mixer', 'compressor']) else 'labor'
                })
            except ValueError:
                continue
    
    # Separate labor and equipment
    labor_crew = [c for c in crew_members if c['type'] == 'labor']
    equipment_crew = [c for c in crew_members if c['type'] == 'equipment']
    
    # Build response
    result = {
        'item': {
            'code': item['full_code'],
            'description': item['description'],
            'unit': item['unit']
        },
        'input': {
            'quantity': quantity,
            'hours_per_day': hours_per_day,
            'number_of_crews': number_of_crews
        },
        'calculations': {
            'total_days': round(total_days, 2),
            'total_hours': round(total_hours, 2),
            'total_man_hours': round(total_man_hours, 2),
            'total_equip_hours': round(total_equip_hours, 2),
            'daily_output': daily_output,  # Per single crew
            'adjusted_daily_output': adjusted_daily_output,  # Total output with all crews
            'man_hours_per_unit': man_hours,
            'equip_hours_per_unit': equip_hours or 0
        },
        'crew': {
            'labor': labor_crew,
            'equipment': equipment_crew,
            'total_labor_count': sum(c['count'] for c in labor_crew),
            'total_equipment_count': len(equipment_crew)
        },
        'activities': [
            {
                'name': 'Site Preparation & Setup',
                'duration_ratio': 0.1,
                'duration_days': round(total_days * 0.1, 2)
            },
            {
                'name': 'Main Work Execution',
                'duration_ratio': 0.7,
                'duration_days': round(total_days * 0.7, 2)
            },
            {
                'name': 'Finishing & Cleanup',
                'duration_ratio': 0.2,
                'duration_days': round(total_days * 0.2, 2)
            }
        ]
    }
    
    return jsonify(result)

@app.route('/api/item/<csi_code>', methods=['GET'])
def get_item(csi_code):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM csi_items WHERE full_code = ?', (csi_code,)).fetchone()
    conn.close()
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(dict(item))

@app.route('/api/item-details', methods=['GET'])
def get_item_details():
    """
    Get complete item details with structured crew information
    Query params: full_code, item_code, or sub2_code
    """
    full_code = request.args.get('full_code')
    item_code = request.args.get('item_code')
    sub2_code = request.args.get('sub2_code')
    
    if not full_code and not item_code and not sub2_code:
        return jsonify({'error': 'full_code, item_code or sub2_code required'}), 400
    
    conn = get_db_connection()
    
    if full_code:
        item = conn.execute('SELECT * FROM csi_items WHERE full_code = ?', (full_code,)).fetchone()
    elif item_code:
        item = conn.execute('SELECT * FROM csi_items WHERE item_code = ?', (item_code,)).fetchone()
    else:
        item = conn.execute('SELECT * FROM csi_items WHERE sub_div2_code = ?', (sub2_code,)).fetchone()
    
    conn.close()

    
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    
    # Build crew details array
    crew_details = []
    for i in range(1, 14):  # Crew 1-13
        crew_num = item[f'crew_num_{i}']
        crew_desc = item[f'crew_desc_{i}']
        
        if crew_num or crew_desc:
            crew_details.append({
                'crew_number': i,
                'quantity': str(crew_num) if crew_num else '',
                'description': str(crew_desc) if crew_desc else ''
            })
    
    # Build response
    result = {
        'item': {
            'full_code': item['full_code'],
            'main_division': {
                'code': item['main_div_code'],
                'name': item['main_div_name']
            },
            'sub_division1': {
                'code': item['sub_div1_code'],
                'name': item['sub_div1_name']
            },
            'sub_division2': {
                'code': item['sub_div2_code'],
                'name': item['sub_div2_name']
            },
            'item_code': item['item_code'],
            'description': item['description'],
            'unit': item['unit']
        },
        'productivity': {
            'daily_output': item['daily_output'],
            'man_hours': item['man_hours'],
            'equip_hours': item['equip_hours'],
            'crew_structure_combined': item['crew_structure']
        },
        'crew_details': crew_details
    }
    
    return jsonify(result)

# --- AI Planner / Assembly Routes ---

@app.route('/api/assemblies', methods=['GET'])
def get_assemblies():
    """List all available assemblies"""
    conn = get_db_connection()
    assemblies = conn.execute('SELECT * FROM assemblies').fetchall()
    conn.close()
    return jsonify([dict(row) for row in assemblies])

@app.route('/api/calculate-assembly', methods=['POST'])
def calculate_assembly():
    """
    Calculate full Bill of Materials & Crew for an Assembly
    Input: { "assembly_id": 1, "quantity": 100 }
    """
    data = request.json
    assembly_id = data.get('assembly_id')
    user_qty = float(data.get('quantity', 0))
    
    if not assembly_id or user_qty <= 0:
        return jsonify({'error': 'Invalid input'}), 400
        
    conn = get_db_connection()
    
    # 1. Get Assembly Info
    assembly = conn.execute('SELECT * FROM assemblies WHERE id = ?', (assembly_id,)).fetchone()
    if not assembly:
        conn.close()
        return jsonify({'error': 'Assembly not found'}), 404
        
    # 2. Get Components
    components = conn.execute('''
        SELECT ac.*, ci.* 
        FROM assembly_components ac
        JOIN csi_items ci ON ac.csi_full_code = ci.full_code
        WHERE ac.assembly_id = ?
    ''', (assembly_id,)).fetchall()
    
    conn.close()
    
    results = []
    total_project_days = 0
    
    for comp in components:
        # Calculate Component Quantity based on Ratio
        # e.g. 100 m3 foundation * 12 m2/m3 = 1200 m2 forms
        comp_qty = user_qty * comp['ratio_to_primary']
        
        # Calculate Productivity (Days)
        # Days = Qty / (Daily Output * num_crews) -> defaulting to 1 crew for now
        daily_output = comp['daily_output'] or 1 # Avoid div by zero
        duration_days = comp_qty / daily_output
        
        # Keep track of max duration if parallel, or sum if sequential.
        # For simplicity in this version, we list them. Real scheduling is complex.
        total_project_days += duration_days 
        
        # Parse Crew (Simplified for the summary view)
        crew_summary = comp['crew_structure'] or "Standard Crew"
        
        results.append({
            'role_en': comp['component_role_en'],
            'role_ar': comp['component_role_ar'],
            'item_code': comp['full_code'],
            'description': comp['description'],
            'calculated_qty': round(comp_qty, 2),
            'unit': comp['unit'],
            'impacting_ratio': comp['ratio_to_primary'],
            'daily_output': daily_output,
            'duration_days': round(duration_days, 2),
            'crew_summary': crew_summary
        })
        
    return jsonify({
        'assembly': dict(assembly),
        'input_qty': user_qty,
        'components': results,
        'estimated_total_duration': round(total_project_days, 2) # Rough sum
    })

# --- Chat / AI Wizard Routes ---

# Import keyword mapping for smart search
from keyword_mapping import KEYWORD_MAPPING, find_matching_keywords

# Import CSI reranker for advanced search
from csi_reranker import rerank_candidates, search_and_rerank

@app.route('/api/rerank', methods=['POST'])
def rerank_api():
    """
    CSI-Based Relevance Reranker API.
    
    Accepts:
    - query: User query text
    - candidates (optional): Pre-fetched candidates to rerank
    - top_n: Number of candidates to fetch (default 50)
    - top_k: Number of results to return (default 7)
    - filters (optional): Hard filters like {division, man_hours_lt}
    
    Returns: JSON with ranked results, warnings, suggestions
    """
    data = request.json
    query = (data.get("query") or "").strip()
    
    if not query:
        return jsonify({
            "query": "",
            "language": "en",
            "top_k": 0,
            "results": [],
            "warnings": ["Query is required"],
            "suggestions": ["Provide a search query like 'isolated footing reinforcement'"],
            "data_source_missing": False
        })
    
    # Check if candidates are provided (external reranking)
    candidates = data.get("candidates")
    
    if candidates:
        # Rerank provided candidates
        top_k = data.get("top_k", 7)
        filters = data.get("filters")
        query_unit = data.get("unit")
        
        result = rerank_candidates(
            query=query,
            candidates=candidates,
            top_k=top_k,
            query_unit=query_unit,
            filters=filters
        )
    else:
        # Full search and rerank pipeline
        top_n = data.get("top_n", 50)
        top_k = data.get("top_k", 7)
        
        result = search_and_rerank(
            query=query,
            top_n=top_n,
            return_top_k=top_k
        )
    
    return jsonify(result)

# Import intelligent AI module
from intelligent_ai import (
    CSI_AI_SYSTEM_PROMPT, CSI_AI_SYSTEM_PROMPT_EN,
    get_csi_context, search_database, calculate_productivity,
    process_ai_response, format_search_results
)

@app.route('/api/intelligent-ai', methods=['POST'])
def intelligent_ai():
    """
    Intelligent AI endpoint powered by Groq AI (Llama 3.3).
    
    Unlike rule-based matching, this endpoint:
    1. Uses real AI to understand natural language
    2. Asks intelligent follow-up questions
    3. Searches database based on AI understanding
    4. Calculates productivity with context awareness
    
    Free tier: 14,400 requests/day!
    """
    data = request.json
    query = (data.get("query") or "").strip()
    lang = data.get("lang", "ar")
    conversation_history = data.get("history", [])
    
    # Normalize language
    lang = 'ar' if 'ar' in lang.lower() else 'en'
    
    # Check if Groq is available
    if not GROQ_CLIENT:
        return jsonify({
            "text": "⚠️ AI غير متاح حالياً. تأكد من إعداد GROQ_API_KEY." if lang == 'ar' else "⚠️ AI is not available. Please configure GROQ_API_KEY.",
            "status": "error"
        })
    
    if not query:
        # Greeting
        if lang == 'ar':
            greeting = (
                "مرحباً! 👋 أنا مساعدك الذكي للأعمال الإنشائية.\n\n"
                "🧠 **أنا أفكر وأفهم!** اسألني بأي طريقة:\n"
                "• 'عايز أحسب كمية خرسانة قاعدة 2×2 متر'\n"
                "• 'كم المدة اللازمة لمحارة 500 متر مربع؟'\n"
                "• 'إيه إنتاجية فريق الحدادة للأعمدة؟'\n\n"
                "💬 اكتب سؤالك وسأساعدك!"
            )
        else:
            greeting = (
                "Hello! 👋 I'm your intelligent construction assistant.\n\n"
                "🧠 **I actually think and understand!** Ask me anything:\n"
                "• 'Calculate concrete for a 2x2m footing'\n"
                "• 'How long to plaster 500 sqm?'\n"
                "• 'What's the productivity for column reinforcement?'\n\n"
                "💬 Type your question and I'll help!"
            )
        return jsonify({
            "text": greeting,
            "status": "greeting"
        })
    
    try:
        # **NEW: CSI Lookup preprocessing**
        from intelligent_ai import preprocess_query_with_csi
        csi_result = preprocess_query_with_csi(query, lang)
        
        # Prepare context with CSI data samples
        csi_context = get_csi_context()
        
        # Select appropriate system prompt
        system_prompt = CSI_AI_SYSTEM_PROMPT if lang == 'ar' else CSI_AI_SYSTEM_PROMPT_EN
        
        # Build conversation for Groq
        full_prompt = f"""{system_prompt}

{csi_context}

## المحادثة السابقة:
{json.dumps(conversation_history[-30:], ensure_ascii=False) if conversation_history else "لا توجد محادثة سابقة"}

## استفسار المستخدم الحالي:
{query}

## ردك (JSON فقط):"""

        # Call Groq AI (much faster and more reliable than Gemini!)
        try:
            response = GROQ_CLIENT.chat.completions.create(
                model=AI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt + "\n\n" + csi_context},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            ai_text = response.choices[0].message.content
        except Exception as api_error:
            error_msg = f"⚠️ حدث خطأ: {str(api_error)}" if lang == 'ar' else f"⚠️ Error: {str(api_error)}"
            return jsonify({"text": error_msg, "status": "error"})
        
        # Process AI response
        ai_data = process_ai_response(ai_text, lang)
        
        if ai_data.get("action") == "search":
            # AI wants to search - do the search
            search_terms = ai_data.get("search_terms", [])
            element_type = ai_data.get("element_type")
            work_stage = ai_data.get("work_stage")
            quantity = ai_data.get("quantity")
            unit = ai_data.get("unit")
            
            # Search database
            results = search_database(search_terms, element_type, work_stage)
            
            if results and quantity:
                # Calculate productivity for first result
                calc = calculate_productivity(results[0], quantity)
                
                if lang == 'ar':
                    text = f"✅ **نتيجة الحساب:**\n\n"
                    text += f"📦 **البند:** {calc['item_description'][:60]}\n"
                    text += f"📏 **الكمية:** {calc['quantity']} {calc['unit']}\n"
                    text += f"⚡ **الإنتاجية:** {calc['daily_output']} {calc['unit']}/يوم\n"
                    text += f"⏱️ **المدة المتوقعة:** {calc['duration_days']} يوم\n"
                    text += f"👷 **ساعات العمل:** {calc['total_man_hours']} ساعة\n"
                    if calc['crew_structure']:
                        text += f"👥 **تشكيل الفريق:** {calc['crew_structure'][:50]}\n"
                else:
                    text = f"✅ **Calculation Result:**\n\n"
                    text += f"📦 **Item:** {calc['item_description'][:60]}\n"
                    text += f"📏 **Quantity:** {calc['quantity']} {calc['unit']}\n"
                    text += f"⚡ **Output:** {calc['daily_output']} {calc['unit']}/day\n"
                    text += f"⏱️ **Duration:** {calc['duration_days']} days\n"
                    text += f"👷 **Man-hours:** {calc['total_man_hours']} hours\n"
                
                return jsonify({
                    "text": text,
                    "status": "result",
                    "calculation": calc,
                    "items": results[:3],
                    "csi_info": csi_result if csi_result.get('has_matches') else None
                })
            else:
                # Show search results
                text = format_search_results(results, lang)
                return jsonify({
                    "text": text,
                    "status": "results",
                    "items": results[:5],
                    "csi_info": csi_result if csi_result.get('has_matches') else None
                })
        
        elif ai_data.get("action") == "ask":
            # AI needs more information
            question = ai_data.get("question", "")
            options = ai_data.get("options", [])
            
            text = question
            if options:
                text += "\n\n"
                for i, opt in enumerate(options, 1):
                    text += f"{i}️⃣ {opt}\n"
            
            return jsonify({
                "text": text,
                "status": "question",
                "options": options,
                "csi_info": csi_result if csi_result.get('has_matches') else None
            })
        
        else:
            # Direct response
            return jsonify({
                "text": ai_data.get("message", ai_text),
                "status": "response"
            })
    
    except Exception as e:
        error_msg = f"⚠️ حدث خطأ: {str(e)}" if lang == 'ar' else f"⚠️ Error: {str(e)}"
        return jsonify({
            "text": error_msg,
            "status": "error"
        })

@app.route('/api/smart-ai', methods=['POST'])
def smart_ai():
    """
    Smart AI endpoint that:
    1. Understands Arabic/English construction queries
    2. Searches CSI database for matching items
    3. Asks for quantity if needed
    4. Returns productivity data with duration calculations
    """
    data = request.json
    query = (data.get("query") or "").strip()
    lang = data.get("lang", "ar")
    quantity = data.get("quantity")  # Optional quantity
    selected_item_code = data.get("item_code")  # Optional item code if user selected one
    
    # Normalize language
    lang = 'ar' if 'ar' in lang else 'en'
    
    if not query and not selected_item_code:
        if lang == 'ar':
            greeting = (
                "مرحباً! 👋 أنا مساعدك الذكي للبحث عن إنتاجيات الأعمال الإنشائية.\n\n"
                "📝 **كيف يمكنني مساعدتك؟**\n"
                "• اكتب نوع العمل مثل: محارة، سيراميك، خرسانة، عزل\n"
                "• حدد الكمية والوحدة للحصول على المدة الزمنية\n"
                "• اسأل عن أي بند إنشائي وسأبحث لك في قاعدة بيانات CSI\n\n"
                "💡 **أمثلة للبحث:**\n"
                "• محارة حوائط\n"
                "• cement plaster\n"
                "• سيراميك أرضيات\n"
                "• خرسانة أعمدة"
            )
        else:
            greeting = (
                "Hello! 👋 I'm your smart assistant for construction productivity data.\n\n"
                "📝 **How can I help you?**\n"
                "• Type a work type like: plastering, tiles, concrete, waterproofing\n"
                "• Specify quantity and unit to get duration estimates\n"
                "• Ask about any construction item and I'll search the CSI database\n\n"
                "💡 **Search Examples:**\n"
                "• wall plaster\n"
                "• cement plaster masonry\n"
                "• ceramic floor tiles\n"
                "• concrete columns"
            )
        return jsonify({
            "text": greeting,
            "status": "greeting"
        })
    
    # If user selected an item and provided quantity, calculate productivity
    if selected_item_code and quantity:
        return calculate_from_csi(selected_item_code, float(quantity), lang)
    
    # Find matching keywords in the query
    matches = find_matching_keywords(query)
    
    # Check if this is a plastering query - offer structured options
    plastering_keywords_ar = ["محارة", "لياسة", "بياض", "طرطشة", "ضهارة"]
    plastering_keywords_en = ["plaster", "plastering", "render", "stucco"]
    
    is_plastering_query = any(kw in query.lower() for kw in plastering_keywords_ar + plastering_keywords_en)
    
    if is_plastering_query:
        # Get all plastering items from database
        conn = get_db_connection()
        plastering_items = conn.execute(
            "SELECT full_code, description, unit, daily_output FROM csi_items "
            "WHERE full_code LIKE '092 102%' OR full_code LIKE '092 304%' "
            "ORDER BY full_code LIMIT 15"
        ).fetchall()
        conn.close()
        
        if plastering_items:
            # Group items by type
            items_list = []
            for item in plastering_items:
                items_list.append({
                    "code": item['full_code'],
                    "description": item['description'],
                    "unit": item['unit'],
                    "daily_output": item['daily_output']
                })
            
            if lang == 'ar':
                response_text = (
                    "🏗️ **أعمال المحارة تتكون من عدة مراحل:**\n\n"
                    "1️⃣ **طرطشة (Splash Coat)** - طبقة الالتصاق الأولى\n"
                    "2️⃣ **فرد المحارة (Brown Coat)** - الطبقة الأساسية\n"
                    "3️⃣ **ضهارة (Finish Coat)** - التنعيم النهائي\n"
                    "4️⃣ **محارة كاملة 3 طبقات** - تشمل كل ما سبق\n\n"
                    "📋 **اختر نوع العمل المطلوب:**"
                )
            else:
                response_text = (
                    "🏗️ **Plastering work consists of several stages:**\n\n"
                    "1️⃣ **Splash Coat** - Initial bonding layer\n"
                    "2️⃣ **Brown Coat** - Main body coat\n"
                    "3️⃣ **Finish Coat** - Final smoothing\n"
                    "4️⃣ **Complete 3 Coats** - All of the above\n\n"
                    "📋 **Select the required work type:**"
                )
            
            return jsonify({
                "text": response_text,
                "status": "select_item",
                "items": items_list,
                "prompt": "اختر نوع المحارة ثم أدخل المساحة بالمتر المربع:" if lang == 'ar' else "Select plaster type then enter area in SQM:"
            })
    
    # Check if this is a concrete element query
    from concrete_mapping import (
        detect_concrete_element, detect_work_stage, 
        CONCRETE_ELEMENTS, WORK_STAGES,
        get_element_options_message, get_work_stage_message
    )
    
    element_key, subtype_key, detected_lang = detect_concrete_element(query)
    work_stage = detect_work_stage(query)
    
    if element_key:
        # User is asking about a concrete element
        element = CONCRETE_ELEMENTS[element_key]
        
        # Check if we need to ask about subtype
        if not subtype_key and element.get("subtypes"):
            # Ask user to select subtype
            if lang == 'ar':
                msg = f"🏗️ **{element['display_ar']}**\n\n"
                msg += "ما نوع العنصر المطلوب؟\n\n"
                for i, (key, data) in enumerate(element['subtypes'].items(), 1):
                    msg += f"• **{data['ar']}** ({data['en']})\n"
                msg += "\n💡 اكتب النوع المطلوب"
            else:
                msg = f"🏗️ **{element['display_en']}**\n\n"
                msg += "What type do you need?\n\n"
                for i, (key, data) in enumerate(element['subtypes'].items(), 1):
                    msg += f"• **{data['en']}** ({data['ar']})\n"
                msg += "\n💡 Type the required type"
            
            return jsonify({
                "text": msg,
                "status": "need_subtype",
                "element_type": element_key,
                "prompt": "اختر نوع العنصر:" if lang == 'ar' else "Select element type:"
            })
        
        # Check if we need to ask about work stage
        if not work_stage:
            # Ask user to select work stage
            if lang == 'ar':
                msg = f"🛠️ **ما نوع العمل المطلوب لـ {element['display_ar']}؟**\n\n"
                msg += "1️⃣ **نجارة / شدات** (Formwork) - أعمال الشدة والفك\n"
                msg += "2️⃣ **حدادة / تسليح** (Reinforcement) - تجهيز وتركيب الحديد\n"
                msg += "3️⃣ **صب خرسانة** (Casting) - صب وتسوية الخرسانة\n"
                msg += "4️⃣ **شامل** (All) - كل المراحل\n\n"
                msg += "💡 اكتب رقم المرحلة أو اسمها"
            else:
                msg = f"🛠️ **What work stage do you need for {element['display_en']}?**\n\n"
                msg += "1️⃣ **Formwork** - Forms and shuttering\n"
                msg += "2️⃣ **Reinforcement** - Rebar work\n"
                msg += "3️⃣ **Concrete Casting** - Pouring and finishing\n"
                msg += "4️⃣ **All Stages** - Complete work\n\n"
                msg += "💡 Type the stage number or name"
            
            return jsonify({
                "text": msg,
                "status": "need_work_stage",
                "element_type": element_key,
                "subtype": subtype_key,
                "prompt": "اختر مرحلة العمل:" if lang == 'ar' else "Select work stage:"
            })
        
        # We have all info, search for items
        conn = get_db_connection()
        
        # Build search based on element and stage
        search_conditions = []
        params = []
        
        if work_stage == "formwork":
            # Search for formwork items
            search_conditions.append("full_code LIKE '031%'")
            if element_key == "column":
                search_conditions.append("description LIKE '%column%'")
            elif element_key == "beam":
                search_conditions.append("(description LIKE '%beam%' OR description LIKE '%girder%')")
            elif element_key == "slab":
                search_conditions.append("description LIKE '%slab%'")
            elif element_key == "footing":
                search_conditions.append("(description LIKE '%footing%' OR description LIKE '%foundation%')")
        elif work_stage == "reinforcement":
            # Search for reinforcement items
            search_conditions.append("full_code LIKE '032%'")
            if element_key == "column":
                search_conditions.append("description LIKE '%column%'")
            elif element_key == "beam":
                search_conditions.append("(description LIKE '%beam%' OR description LIKE '%girder%')")
            elif element_key == "slab":
                search_conditions.append("description LIKE '%slab%'")
            elif element_key == "footing":
                search_conditions.append("description LIKE '%footing%'")
        elif work_stage == "casting":
            # Search for casting/concrete items
            search_conditions.append("full_code LIKE '033%'")
        else:
            # All stages - search by element type
            if element_key == "column":
                search_conditions.append("description LIKE '%column%'")
            elif element_key == "beam":
                search_conditions.append("(description LIKE '%beam%' OR description LIKE '%girder%')")
            elif element_key == "footing":
                search_conditions.append("(description LIKE '%footing%' OR description LIKE '%foundation%')")
            elif element_key == "slab":
                search_conditions.append("description LIKE '%slab%'")
        
        where_clause = " AND ".join(search_conditions) if search_conditions else "1=1"
        sql = f"SELECT full_code, description, unit, daily_output FROM csi_items WHERE {where_clause} LIMIT 15"
        
        items = conn.execute(sql).fetchall()
        conn.close()
        
        if items:
            items_list = [{
                "code": item['full_code'],
                "description": item['description'],
                "unit": item['unit'],
                "daily_output": item['daily_output']
            } for item in items]
            
            stage_name = WORK_STAGES.get(work_stage, {}).get('ar' if lang == 'ar' else 'en', work_stage)
            
            if lang == 'ar':
                msg = f"📋 **نتائج البحث - {element['display_ar']} ({stage_name})**\n\n"
                msg += f"وجدت {len(items)} بند مطابق.\n"
                msg += "اختر البند المناسب ثم أدخل:\n"
                msg += "• **الكمية** بالوحدة المحددة\n"
                msg += "• **عدد فرق العمل** (اختياري)"
            else:
                msg = f"📋 **Search Results - {element['display_en']} ({stage_name})**\n\n"
                msg += f"Found {len(items)} matching items.\n"
                msg += "Select an item then enter:\n"
                msg += "• **Quantity** in the specified unit\n"
                msg += "• **Number of crews** (optional)"
            
            return jsonify({
                "text": msg,
                "status": "select_item",
                "items": items_list,
                "element_type": element_key,
                "work_stage": work_stage,
                "prompt": "اختر البند وأدخل الكمية:" if lang == 'ar' else "Select item and enter quantity:"
            })
        else:
            return search_csi_database(query, lang)
    
    if not matches:
        # Try direct database search
        return search_csi_database(query, lang)
    
    # Get the best match
    best_match = matches[0]
    csi_search = best_match.get("csi_search", best_match.get("en", [""])[0])
    unit = best_match.get("unit", "m2")
    
    # Search database for matching items
    conn = get_db_connection()
    
    # Search by description
    items = conn.execute(
        "SELECT full_code, description, unit, daily_output, man_hours, equip_hours, crew_structure "
        "FROM csi_items WHERE description LIKE ? OR description LIKE ? LIMIT 10",
        (f'%{csi_search}%', f'%{best_match.get("en", [""])[0]}%')
    ).fetchall()
    
    conn.close()
    
    if not items:
        # Fallback to broader search
        return search_csi_database(query, lang)
    
    # If quantity is provided, calculate for the first matching item
    if quantity and items:
        item = items[0]
        return calculate_productivity_response(item, float(quantity), lang, best_match)
    
    # Build items list with ACTUAL units from database
    items_list = []
    for item in items[:5]:  # Limit to 5 items
        items_list.append({
            "code": item['full_code'],
            "description": item['description'],
            "unit": item['unit'],  # Actual unit from DB
            "daily_output": item['daily_output']
        })
    
    # Get units info for display - collect unique units from results
    unique_units = list(set([i['unit'] for i in items if i['unit']]))
    
    if lang == 'ar':
        if len(unique_units) == 1:
            unit_display = unique_units[0]
            response_text = f"وجدت {len(items)} بند مطابق لـ \"{query}\". اختر البند المناسب ثم أدخل الكمية بوحدة ({unit_display})."
        else:
            response_text = f"وجدت {len(items)} بند مطابق لـ \"{query}\". اختر البند المناسب ثم أدخل الكمية بالوحدة المحددة لكل بند."
    else:
        if len(unique_units) == 1:
            unit_display = unique_units[0]
            response_text = f"Found {len(items)} matching items for \"{query}\". Select an item and enter quantity in ({unit_display})."
        else:
            response_text = f"Found {len(items)} items for \"{query}\". Select an item and enter quantity in the specified unit."
    
    return jsonify({
        "text": response_text,
        "status": "select_item",  # Changed to select_item - user should pick first
        "matched_type": best_match.get("key"),
        "items": items_list,
        "prompt": "اختر بند ثم أدخل الكمية:" if lang == 'ar' else "Select an item then enter quantity:"
    })

def search_csi_database(query, lang):
    """Search CSI database directly"""
    conn = get_db_connection()
    
    items = conn.execute(
        "SELECT full_code, description, unit, daily_output, man_hours FROM csi_items "
        "WHERE description LIKE ? OR full_code LIKE ? LIMIT 10",
        (f'%{query}%', f'%{query}%')
    ).fetchall()
    
    conn.close()
    
    if not items:
        return jsonify({
            "text": "لم أجد بنود مطابقة. جرب البحث بكلمات مختلفة مثل: concrete, plaster, tiles" if lang == 'ar' else "No matching items found. Try searching with different keywords like: concrete, plaster, tiles",
            "status": "not_found"
        })
    
    items_list = [{"code": i['full_code'], "description": i['description'], "unit": i['unit'], "daily_output": i['daily_output']} for i in items[:5]]
    
    return jsonify({
        "text": f"وجدت {len(items)} بند. اختر واحداً وحدد الكمية:" if lang == 'ar' else f"Found {len(items)} items. Select one and specify quantity:",
        "status": "select_item",
        "items": items_list
    })

def calculate_from_csi(item_code, quantity, lang):
    """Calculate productivity from CSI item code"""
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM csi_items WHERE full_code = ?", (item_code,)).fetchone()
    conn.close()
    
    if not item:
        return jsonify({"text": "البند غير موجود", "status": "error"})
    
    return calculate_productivity_response(item, quantity, lang, None)

def calculate_productivity_response(item, quantity, lang, match_info):
    """Generate productivity response with calculations"""
    daily_output = item['daily_output'] or 1
    man_hours = item['man_hours'] or 0
    
    # Calculate duration
    duration_days = math.ceil(quantity / daily_output)
    total_man_hours = quantity * man_hours
    
    unit = item['unit']
    unit_ar = {"C.Y.": "م³", "S.F.": "م²", "L.F.": "م.ط", "Ea.": "عدد"}.get(unit, unit)
    
    if lang == 'ar':
        text = (
            f"📊 **نتائج حساب الإنتاجية:**\n\n"
            f"📦 البند: {item['description']}\n"
            f"📐 الكمية: {quantity} {unit_ar}\n"
            f"⚡ الإنتاجية اليومية: {daily_output} {unit_ar}/يوم\n"
            f"⏱️ المدة المتوقعة: **{duration_days} يوم**\n"
            f"👷 ساعات العمل: {total_man_hours:.1f} ساعة\n"
            f"🔧 فريق العمل: {item['crew_structure'] or 'فريق قياسي'}"
        )
    else:
        text = (
            f"📊 **Productivity Calculation Results:**\n\n"
            f"📦 Item: {item['description']}\n"
            f"📐 Quantity: {quantity} {unit}\n"
            f"⚡ Daily Output: {daily_output} {unit}/day\n"
            f"⏱️ Expected Duration: **{duration_days} days**\n"
            f"👷 Man-Hours: {total_man_hours:.1f} hours\n"
            f"🔧 Crew: {item['crew_structure'] or 'Standard Crew'}"
        )
    
    return jsonify({
        "text": text,
        "status": "calculated",
        "result": {
            "item_code": item['full_code'],
            "description": item['description'],
            "quantity": quantity,
            "unit": unit,
            "daily_output": daily_output,
            "duration_days": duration_days,
            "total_man_hours": round(total_man_hours, 1),
            "crew_structure": item['crew_structure']
        }
    })

COURSE_CONTEXT = """
You are an expert Construction Planning Engineer Assistant. Your goal is to help the user find the correct CSI codes and crews for their work.
You have access to a database of CSI items.
The user might ask vague questions like "I need to pour concrete".
You must ask clarifying questions to narrow down the scope (e.g., "Is it for foundations, slabs, or columns?", "What is the compressive strength?").
Once you are confident you know what they need, you can search the database.

To search the database, you must output a JSON object in this EXACT format (no other text):
{
  "search_query": "concrete slab 30mpa",
  "search_type": "item"
}
"""

def query_ollama(messages):
    model = get_working_model()
    try:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        res = requests.post(OLLAMA_API_URL, json=payload)
        if res.status_code == 200:
            return res.json()['message']['content']
        else:
            return f"Error from Ollama (Model: {model}): {res.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

@app.route('/api/chat', methods=['POST'])
def chat_wizard():
    data = request.json
    user_msg = data.get('message')
    history = data.get('history', [])
    
    # 1. Construct Context
    # We append the system prompt at the start if not present
    if not history:
        history.append({"role": "system", "content": COURSE_CONTEXT})
    
    history.append({"role": "user", "content": user_msg})
    
    # 2. Get LLM Response
    llm_response = query_ollama(history)
    
    # 3. Check for Tool Use (JSON)
    # Simple heuristic: does it start with { and contain "search_query"?
    if llm_response.strip().startswith('{') and '"search_query"' in llm_response:
        try:
            cmd = json.loads(llm_response)
            query = cmd['search_query']
            
            # Execute DB Search
            conn = get_db_connection()
            # Simple broad search
            items = conn.execute("SELECT * FROM csi_items WHERE description LIKE ? LIMIT 5", ('%' + query + '%',)).fetchall()
            conn.close()
            
            results = [dict(r) for r in items]
            
            # Return structured result to frontend (handled specially by frontend)
            return jsonify({
                "response": "Here are the matching items I found:",
                "history": history + [{"role": "assistant", "content": llm_response}],
                "results": results,
                "is_final": True
            })
            
        except Exception as e:
            # Fallback if invalid JSON
            print(f"JSON Parse Error: {e}")
            pass

    # Standard Text Response
    history.append({"role": "assistant", "content": llm_response})
    return jsonify({
        "response": llm_response,
        "history": history
    })

@app.route("/api/ai", methods=["POST"])
def ai():
    data = request.json
    query = (data.get("query") or "").strip()
    lang = data.get("lang") or "ar"
    
    # Simple lang normalization
    if 'ar' in lang: lang = 'ar'
    else: lang = 'en'
    
    qty, unit, scope = parse_query(query)

    # Route to appropriate planning function based on detected scope
    if qty:
        if scope == "isolated_foundations":
            return jsonify(plan_isolated_foundations(qty, lang))
        elif scope == "raft_foundation":
            return jsonify(plan_raft_foundation(qty, lang))
        elif scope == "strip_foundation":
            return jsonify(plan_strip_foundation(qty, lang))
        elif scope == "piles":
            return jsonify(plan_pile_foundation(int(qty), lang))
        elif scope == "columns":
            return jsonify(plan_columns(qty, lang))
        elif scope == "beams":
            return jsonify(plan_beams(qty, lang))
        elif scope == "slabs":
            return jsonify(plan_slabs(qty, lang))

    # Use Gemini AI for intelligent conversation if available
    if GEMINI_MODEL:
        try:
            system_prompt = """أنت مساعد ذكي متخصص في هندسة البناء والتخطيط للمشاريع الإنشائية.
            
مهامك:
1. مساعدة المستخدم في تخطيط أعمال البناء
2. تقدير فرق العمل والمدد الزمنية
3. الإجابة على أسئلة متعلقة بـ:
   - الأساسات (منفصلة، شريطية، لبشة، خوازيق)
   - العناصر الإنشائية (أعمدة، كمرات، بلاطات)
   - الخرسانة والتسليح
   - إدارة المشاريع الإنشائية

إذا أراد المستخدم حساب دقيق، اطلب منه ذكر الكمية والوحدة مثل: "أعمدة 50 م³" أو "columns 50 m3"

أجب بشكل مختصر ومفيد. إذا كان السؤال بالإنجليزية، أجب بالإنجليزية.
"""
            
            full_prompt = f"{system_prompt}\n\nسؤال المستخدم: {query}"
            
            response = GEMINI_MODEL.generate_content(full_prompt)
            ai_response = response.text
            
            return jsonify({
                "text": ai_response,
                "notes": "💡 للحصول على خطة مفصلة، اذكر الكمية مثل: أعمدة 50 م³" if lang == "ar" else "💡 For a detailed plan, include quantity like: columns 50 m3"
            })
        except Exception as e:
            print(f"Gemini API Error: {e}")
            # Fallthrough to default response
    
    # Fallback response if Gemini not available or failed
    if lang == "ar":
        return jsonify({
            "text": "مرحباً! أنا مساعد التخطيط الإنشائي. للحصول على خطة تفصيلية، اكتب الكمية والنوع مثل:",
            "notes": (
                "📦 أساسات منفصلة 100 م³\n"
                "🏗️ لبشة 200 م³\n"
                "📏 أساسات شريطية 80 م³\n"
                "🔩 خوازيق 50 خازوق\n"
                "🏛️ أعمدة 30 م³\n"
                "📐 كمرات 40 م³\n"
                "🏠 بلاطة 60 م³"
            )
        })
    else:
        return jsonify({
            "text": "Hello! I'm a construction planning assistant. For a detailed plan, include the quantity and type like:",
            "notes": (
                "📦 Isolated foundations 100 m3\n"
                "🏗️ Raft foundation 200 m3\n"
                "📏 Strip foundation 80 m3\n"
                "🔩 Piles 50 piles\n"
                "🏛️ Columns 30 m3\n"
                "📐 Beams 40 m3\n"
                "🏠 Slab 60 m3"
            )
        })

# --- End Chat Routes ---

# Serve frontend files
# Determine frontend path (Local vs Production)
local_static = os.path.join(os.path.dirname(__file__), 'static_files')
parent_frontend = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')

if os.path.exists(local_static):
    FRONTEND_PATH = local_static  # Production (Railway/Render)
else:
    FRONTEND_PATH = parent_frontend  # Local Dev

print(f"[INFO] Serving frontend from: {FRONTEND_PATH}")

@app.route('/')

def index():
    return send_from_directory(FRONTEND_PATH, 'index.html')
@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory(FRONTEND_PATH, path)

if __name__ == '__main__':
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
