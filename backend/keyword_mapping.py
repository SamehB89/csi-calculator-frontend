# Keyword Mapping: Arabic → English → CSI Division
# Used by AI Wizard to understand user queries and map to CSI database

KEYWORD_MAPPING = {
    # === FOUNDATIONS (Division 03) ===
    "foundations": {
        "ar": ["قواعد", "أساسات", "اساسات", "قاعدة", "أساس"],
        "en": ["foundation", "foundations", "footing", "footings"],
        "csi_division": "03",
        "unit": "m3",
        "unit_ar": "م³"
    },
    "isolated_foundation": {
        "ar": ["قواعد منفصلة", "قاعدة منفصلة", "منفصلة", "منفصل"],
        "en": ["isolated", "pad", "pad footing"],
        "csi_search": "footing isolated",
        "csi_division": "03",
        "unit": "m3"
    },
    "strip_foundation": {
        "ar": ["قواعد شريطية", "شريطي", "شريطية", "سملات", "سمل"],
        "en": ["strip", "continuous", "strip footing"],
        "csi_search": "strip footing",
        "csi_division": "03",
        "unit": "m3"
    },
    "raft_foundation": {
        "ar": ["لبشة", "لبشه", "حصيرة", "رافت"],
        "en": ["raft", "mat", "mat foundation"],
        "csi_search": "mat foundation",
        "csi_division": "03",
        "unit": "m3"
    },
    "piles": {
        "ar": ["خوازيق", "خازوق", "اوتاد"],
        "en": ["pile", "piles", "caisson"],
        "csi_search": "pile",
        "csi_division": "03",
        "unit": "each"
    },
    
    # === STRUCTURAL ELEMENTS (Division 03) ===
    "columns": {
        "ar": ["اعمدة", "أعمدة", "عمود"],
        "en": ["column", "columns"],
        "csi_search": "column concrete",
        "csi_division": "03",
        "unit": "m3"
    },
    "beams": {
        "ar": ["كمرات", "كمرة", "جسور", "جسر"],
        "en": ["beam", "beams"],
        "csi_search": "beam concrete",
        "csi_division": "03",
        "unit": "m3"
    },
    "slabs": {
        "ar": ["بلاطة", "بلاطات", "سقف", "أسقف", "اسقف"],
        "en": ["slab", "slabs", "floor"],
        "csi_search": "slab concrete",
        "csi_division": "03",
        "unit": "m3"
    },
    "tie_beams": {
        "ar": ["سملات", "سمل", "ميدة", "ميد"],
        "en": ["tie beam", "grade beam", "strap beam"],
        "csi_search": "grade beam",
        "csi_division": "03",
        "unit": "m3"
    },
    "stairs": {
        "ar": ["سلالم", "سلم", "درج"],
        "en": ["stairs", "stair", "steps", "landing"],
        "csi_search": "stair concrete",
        "csi_division": "03",
        "unit": "m3"
    },
    "walls": {
        "ar": ["حوائط", "جدران", "جدار", "حائط"],
        "en": ["wall", "walls"],
        "csi_search": "wall concrete",
        "csi_division": "03",
        "unit": "m3"
    },
    
    # === FORMWORK (Division 03) ===
    "formwork": {
        "ar": ["شدة", "شدات", "نجارة مسلحة"],
        "en": ["formwork", "form", "forms", "shuttering"],
        "csi_search": "formwork",
        "csi_division": "03",
        "unit": "m2"
    },
    
    # === WATERPROOFING (Division 07) ===
    "waterproofing": {
        "ar": ["عزل مائي", "عزل", "عازل"],
        "en": ["waterproofing", "waterproof", "damp proof"],
        "csi_search": "waterproofing membrane",
        "csi_division": "07",
        "unit": "m2"
    },
    "bituminous": {
        "ar": ["بيتوميني", "زفتي", "بيتومين"],
        "en": ["bituminous", "bitumen", "asphalt"],
        "csi_search": "bituminous membrane",
        "csi_division": "07",
        "unit": "m2"
    },
    
    # === INSULATION (Division 07) ===
    "thermal_insulation": {
        "ar": ["عزل حراري", "فوم", "بوليسترين"],
        "en": ["thermal insulation", "insulation", "eps", "xps"],
        "csi_search": "thermal insulation",
        "csi_division": "07",
        "unit": "m2"
    },
    
    # === PLASTERING (Division 09) ===
    # Most common: Cement plaster on masonry walls (brick/block)
    "plastering": {
        "ar": ["محارة", "لياسة", "بياض"],
        "en": ["plaster", "plastering", "render", "rendering"],
        "csi_search": "cement plaster",  # Changed to cement plaster (most common)
        "csi_division": "09",
        "unit": "m2"
    },
    "cement_plaster_masonry": {
        "ar": ["محارة اسمنتية", "محارة طوب", "بياض مباني", "محارة مباني"],
        "en": ["cement plaster", "cement render", "masonry plaster"],
        "csi_search": "cement plaster masonry",
        "csi_division": "09",
        "unit": "m2"
    },
    "wall_plaster": {
        "ar": ["محارة حوائط", "بياض حوائط", "لياسة حوائط"],
        "en": ["wall plaster", "wall plastering"],
        "csi_search": "cement plaster interior",  # Interior masonry walls
        "csi_division": "09",
        "unit": "m2"
    },
    "ceiling_plaster": {
        "ar": ["محارة اسقف", "بياض اسقف", "لياسة سقف"],
        "en": ["ceiling plaster", "ceiling plastering"],
        "csi_search": "plaster ceilings",
        "csi_division": "09",
        "unit": "m2"
    },
    "gypsum_plaster": {
        "ar": ["محارة جبسية", "جبس", "محارة جبس"],
        "en": ["gypsum plaster", "gypsum"],
        "csi_search": "gypsum plaster",
        "csi_division": "09",
        "unit": "m2"
    },
    "base_coat": {
        "ar": ["محارة خشنة", "طبقة اساس", "رشة", "طرطشة"],
        "en": ["base coat", "scratch coat", "rough coat", "splash coat"],
        "csi_search": "splash coat",
        "csi_division": "09",
        "unit": "m2"
    },
    "finish_coat": {
        "ar": ["محارة ناعمة", "تشطيب", "طبقة نهائية", "ضهارة"],
        "en": ["finish coat", "skim coat", "final coat", "float finish"],
        "csi_search": "finish coat",
        "csi_division": "09",
        "unit": "m2"
    },
    "stucco": {
        "ar": ["ستوكو", "محارة خارجية"],
        "en": ["stucco", "external render"],
        "csi_search": "stucco",
        "csi_division": "09",
        "unit": "m2"
    },
    
    # === FLOORING (Division 09) ===
    "ceramic_tiles": {
        "ar": ["سيراميك", "بلاط", "كاشي"],
        "en": ["ceramic", "tiles", "tile"],
        "csi_search": "ceramic tile",
        "csi_division": "09",
        "unit": "m2"
    },
    "porcelain_tiles": {
        "ar": ["بورسلان", "بورسلين"],
        "en": ["porcelain"],
        "csi_search": "porcelain tile",
        "csi_division": "09",
        "unit": "m2"
    },
    "marble": {
        "ar": ["رخام"],
        "en": ["marble"],
        "csi_search": "marble",
        "csi_division": "09",
        "unit": "m2"
    },
    "granite": {
        "ar": ["جرانيت", "غرانيت"],
        "en": ["granite"],
        "csi_search": "granite",
        "csi_division": "09",
        "unit": "m2"
    },
    
    # === PAINTING (Division 09) ===
    "painting": {
        "ar": ["دهانات", "دهان", "بوية", "طلاء"],
        "en": ["paint", "painting", "coating"],
        "csi_search": "paint",
        "csi_division": "09",
        "unit": "m2"
    },
    
    # === GYPSUM (Division 09) ===
    "gypsum_board": {
        "ar": ["جبسون بورد", "جبس بورد", "جبس"],
        "en": ["gypsum board", "drywall", "plasterboard"],
        "csi_search": "gypsum board",
        "csi_division": "09",
        "unit": "m2"
    },
    "suspended_ceiling": {
        "ar": ["أسقف معلقة", "سقف معلق", "فورسيلنج"],
        "en": ["suspended ceiling", "false ceiling", "drop ceiling"],
        "csi_search": "suspended ceiling",
        "csi_division": "09",
        "unit": "m2"
    }
}

def find_matching_keywords(query):
    """Find matching work items from user query"""
    query_lower = query.lower()
    matches = []
    
    for key, data in KEYWORD_MAPPING.items():
        # Check Arabic keywords
        for ar_kw in data.get("ar", []):
            if ar_kw in query_lower:
                matches.append({
                    "key": key,
                    "matched_keyword": ar_kw,
                    "language": "ar",
                    **data
                })
                break
        
        # Check English keywords
        for en_kw in data.get("en", []):
            if en_kw in query_lower:
                matches.append({
                    "key": key,
                    "matched_keyword": en_kw,
                    "language": "en",
                    **data
                })
                break
    
    return matches
