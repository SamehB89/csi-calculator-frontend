# -*- coding: utf-8 -*-
"""
Concrete Elements Mapping for Smart AI Conversation Flow
Maps Arabic/English keywords to CSI Division 03 elements (Footings, Columns, Beams, Slabs)
"""

# Concrete element types with subtypes
CONCRETE_ELEMENTS = {
    "footing": {
        "ar": ["قاعدة", "قواعد", "أساس", "أساسات", "فوتنج", "قاعده"],
        "en": ["footing", "foundation", "spread footing", "isolated footing", "pad footing"],
        "display_ar": "قواعد / أساسات",
        "display_en": "Footings / Foundations",
        "subtypes": {
            "isolated": {
                "ar": "قاعدة منفصلة",
                "en": "Isolated/Spread Footing",
                "keywords_ar": ["منفصلة", "منفصله", "سبريد"],
                "keywords_en": ["isolated", "spread", "pad"]
            },
            "strip": {
                "ar": "قاعدة شريطية",
                "en": "Strip/Continuous Footing",
                "keywords_ar": ["شريطية", "شريطيه", "مستمرة"],
                "keywords_en": ["strip", "continuous", "wall footing"]
            },
            "raft": {
                "ar": "لبشة / حصيرة",
                "en": "Raft/Mat Foundation",
                "keywords_ar": ["لبشة", "لبشه", "حصيرة", "مات"],
                "keywords_en": ["raft", "mat", "mat foundation"]
            }
        }
    },
    "column": {
        "ar": ["عمود", "أعمدة", "كولون", "اعمده"],
        "en": ["column", "columns"],
        "display_ar": "أعمدة",
        "display_en": "Columns",
        "subtypes": {
            "square": {
                "ar": "عمود مربع",
                "en": "Square Column",
                "keywords_ar": ["مربع", "مربعة"],
                "keywords_en": ["square"]
            },
            "rectangular": {
                "ar": "عمود مستطيل",
                "en": "Rectangular Column",
                "keywords_ar": ["مستطيل", "مستطيلة"],
                "keywords_en": ["rectangular", "rectangle"]
            },
            "round": {
                "ar": "عمود دائري",
                "en": "Round/Circular Column",
                "keywords_ar": ["دائري", "دائرية", "مستدير"],
                "keywords_en": ["round", "circular", "circle"]
            }
        }
    },
    "beam": {
        "ar": ["كمرة", "كمرات", "بيم", "كمره"],
        "en": ["beam", "beams", "girder", "girders"],
        "display_ar": "كمرات",
        "display_en": "Beams",
        "subtypes": {
            "interior": {
                "ar": "كمرة داخلية",
                "en": "Interior Beam",
                "keywords_ar": ["داخلية", "داخليه"],
                "keywords_en": ["interior", "internal"]
            },
            "spandrel": {
                "ar": "كمرة خارجية / ساقطة",
                "en": "Spandrel/External Beam",
                "keywords_ar": ["خارجية", "ساقطة", "ساقطه"],
                "keywords_en": ["spandrel", "external", "exterior"]
            },
            "grade": {
                "ar": "سمل / ميدة",
                "en": "Grade Beam / Tie Beam",
                "keywords_ar": ["سمل", "ميدة", "ميده", "رباط"],
                "keywords_en": ["grade beam", "tie beam", "strap"]
            }
        }
    },
    "slab": {
        "ar": ["سقف", "بلاطة", "سلاب", "اسقف", "بلاطه"],
        "en": ["slab", "floor", "elevated slab", "roof slab"],
        "display_ar": "أسقف / بلاطات",
        "display_en": "Slabs",
        "subtypes": {
            "flat": {
                "ar": "سقف مسطح (فلات سلاب)",
                "en": "Flat Slab",
                "keywords_ar": ["مسطح", "فلات"],
                "keywords_en": ["flat", "flat slab"]
            },
            "solid": {
                "ar": "سقف صلب",
                "en": "Solid Slab",
                "keywords_ar": ["صلب", "صلبة"],
                "keywords_en": ["solid"]
            },
            "on_grade": {
                "ar": "أرضية خرسانية",
                "en": "Slab on Grade",
                "keywords_ar": ["أرضية", "ارضيه", "على التربة"],
                "keywords_en": ["on grade", "ground", "floor slab"]
            },
            "elevated": {
                "ar": "سقف علوي",
                "en": "Elevated Slab",
                "keywords_ar": ["علوي", "مرتفع"],
                "keywords_en": ["elevated", "suspended"]
            }
        }
    },
    "wall": {
        "ar": ["حائط", "جدار", "حوائط", "جدران"],
        "en": ["wall", "walls", "shear wall"],
        "display_ar": "حوائط خرسانية",
        "display_en": "Concrete Walls",
        "subtypes": {
            "shear": {
                "ar": "حائط قص",
                "en": "Shear Wall",
                "keywords_ar": ["قص", "قصي"],
                "keywords_en": ["shear"]
            },
            "retaining": {
                "ar": "حائط استنادي",
                "en": "Retaining Wall",
                "keywords_ar": ["استنادي", "استناديه", "ساند"],
                "keywords_en": ["retaining", "retention"]
            }
        }
    }
}

# Work stages with CSI code prefixes
WORK_STAGES = {
    "formwork": {
        "ar": "نجارة / شدات",
        "en": "Formwork",
        "code_prefix": "031",
        "keywords_ar": ["نجارة", "شدة", "شدات", "فورم"],
        "keywords_en": ["formwork", "form", "forms", "shuttering"]
    },
    "reinforcement": {
        "ar": "حدادة / تسليح",
        "en": "Reinforcement",
        "code_prefix": "032",
        "keywords_ar": ["حدادة", "تسليح", "حديد"],
        "keywords_en": ["reinforcement", "rebar", "steel", "reinforcing"]
    },
    "casting": {
        "ar": "صب خرسانة",
        "en": "Concrete Casting",
        "code_prefix": "033",
        "keywords_ar": ["صب", "خرسانة", "خرسانه"],
        "keywords_en": ["casting", "concrete", "pour", "pouring", "placing"]
    },
    "all": {
        "ar": "شامل (الكل)",
        "en": "All Stages (Complete)",
        "code_prefix": None,
        "keywords_ar": ["شامل", "كامل", "كل"],
        "keywords_en": ["all", "complete", "full", "everything"]
    }
}


def detect_concrete_element(query):
    """
    Detect which concrete element the user is asking about.
    Returns: (element_key, subtype_key or None, detected_language)
    """
    query_lower = query.lower()
    
    for element_key, element_data in CONCRETE_ELEMENTS.items():
        # Check Arabic keywords
        for kw in element_data["ar"]:
            if kw in query_lower:
                # Check for subtype
                subtype = detect_subtype(query_lower, element_data.get("subtypes", {}))
                return (element_key, subtype, "ar")
        
        # Check English keywords
        for kw in element_data["en"]:
            if kw in query_lower:
                subtype = detect_subtype(query_lower, element_data.get("subtypes", {}))
                return (element_key, subtype, "en")
    
    return (None, None, None)


def detect_subtype(query, subtypes):
    """Detect specific subtype from query."""
    for subtype_key, subtype_data in subtypes.items():
        for kw in subtype_data.get("keywords_ar", []):
            if kw in query:
                return subtype_key
        for kw in subtype_data.get("keywords_en", []):
            if kw in query:
                return subtype_key
    return None


def detect_work_stage(query):
    """Detect which work stage the user is asking about."""
    query_lower = query.lower()
    
    for stage_key, stage_data in WORK_STAGES.items():
        for kw in stage_data.get("keywords_ar", []):
            if kw in query_lower:
                return stage_key
        for kw in stage_data.get("keywords_en", []):
            if kw in query_lower:
                return stage_key
    
    return None


def get_element_options_message(element_key, lang):
    """Generate message asking user to select element subtype."""
    element = CONCRETE_ELEMENTS.get(element_key)
    if not element:
        return None
    
    subtypes = element.get("subtypes", {})
    
    if lang == "ar":
        msg = f"🏗️ **{element['display_ar']}**\n\n"
        msg += "ما نوع العنصر المطلوب؟\n\n"
        for i, (key, data) in enumerate(subtypes.items(), 1):
            msg += f"{i}️⃣ **{data['ar']}** ({data['en']})\n"
    else:
        msg = f"🏗️ **{element['display_en']}**\n\n"
        msg += "What type do you need?\n\n"
        for i, (key, data) in enumerate(subtypes.items(), 1):
            msg += f"{i}️⃣ **{data['en']}** ({data['ar']})\n"
    
    return msg


def get_work_stage_message(lang):
    """Generate message asking user to select work stage."""
    if lang == "ar":
        msg = "🛠️ **ما نوع العمل المطلوب؟**\n\n"
        msg += "1️⃣ **نجارة / شدات** (Formwork)\n"
        msg += "2️⃣ **حدادة / تسليح** (Reinforcement)\n"
        msg += "3️⃣ **صب خرسانة** (Casting)\n"
        msg += "4️⃣ **شامل** (All Stages)"
    else:
        msg = "🛠️ **What type of work do you need?**\n\n"
        msg += "1️⃣ **Formwork** (نجارة / شدات)\n"
        msg += "2️⃣ **Reinforcement** (حدادة / تسليح)\n"
        msg += "3️⃣ **Concrete Casting** (صب خرسانة)\n"
        msg += "4️⃣ **All Stages** (شامل)"
    
    return msg


def build_search_query(element_key, subtype_key, stage_key):
    """Build database search query based on selections."""
    search_terms = []
    
    element = CONCRETE_ELEMENTS.get(element_key)
    if element:
        # Add element type to search
        if element_key == "footing":
            search_terms.extend(["footing", "foundation"])
        elif element_key == "column":
            search_terms.append("column")
        elif element_key == "beam":
            search_terms.extend(["beam", "girder"])
        elif element_key == "slab":
            search_terms.append("slab")
        elif element_key == "wall":
            search_terms.append("wall")
        
        # Add subtype specifics
        if subtype_key:
            subtype = element.get("subtypes", {}).get(subtype_key, {})
            if subtype_key == "round":
                search_terms.append("round")
            elif subtype_key == "grade":
                search_terms.append("grade beam")
    
    return search_terms
