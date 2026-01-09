"""
Extract data from 'مساعد المساعد الذكي.xlsx' and convert to enhanced JSON format
for integration with AI Chat Wizard CSI Lookup system.
"""
import pandas as pd
import json
import re
from pathlib import Path

# File paths
EXCEL_FILE = r'd:\SUPERMANn\CSI_Project\مساعد المساعد الذكي.xlsx'
OUTPUT_JSON = r'd:\SUPERMANn\CSI_Project\frontend\data\csi-lookup-database-enhanced.json'
EXISTING_JSON = r'd:\SUPERMANn\CSI_Project\frontend\data\csi-lookup-database.json'

def clean_text(text):
    """Clean and normalize text"""
    if pd.isna(text):
        return ""
    return str(text).strip()

def extract_activities(text):
    """Extract activities from text, splitting by common delimiters"""
    if not text:
        return []
    # Split by comma, semicolon, or newline
    activities = re.split(r'[,;،\n]', text)
    return [a.strip() for a in activities if a.strip()]

def parse_excel_data():
    """Parse the Excel file and extract structured data"""
    print("📖 Reading Excel file...")
    df = pd.read_excel(EXCEL_FILE, sheet_name='Sheet1', header=None)
    
    # Initialize data structure
    enhanced_items = []
    current_category = None
    current_category_id = None
    
    category_map = {
        'أعمال الخرسانة': ('concrete', 'Concrete Works'),
        'الأعمال الترابية': ('earthworks', 'Earthworks'),
        'أعمال النزح': ('dewatering', 'Dewatering'),
        'أعمال العزل': ('waterproofing', 'Waterproofing'),
        'التشطيبات': ('finishes', 'Finishes'),
        'أعمال تكميلية': ('supplementary', 'Supplementary Works'),
        'السباكة': ('plumbing', 'Plumbing')
    }
    
    print("🔍 Parsing rows...")
    
    for idx, row in df.iterrows():
        col0 = clean_text(row[0]) if len(row) > 0 else ""
        col1 = clean_text(row[1]) if len(row) > 1 else ""
        col2 = clean_text(row[2]) if len(row) > 2 else ""
        col3 = clean_text(row[3]) if len(row) > 3 else ""
        
        # Skip empty rows
        if not col0:
            continue
            
        # Check for category headers
        for ar_cat, (cat_id, en_cat) in category_map.items():
            if ar_cat in col0 or f'جدول {ar_cat}' in col0:
                current_category = ar_cat
                current_category_id = cat_id
                print(f"  📁 Category: {ar_cat}")
                break
        
        # Skip header rows and definitions
        if 'البند' in col0 or 'تعريف' in col0 or 'ملاحظة تنفيذية' in col0 or 'سؤال المستخدم' in col0:
            continue
        if 'جدول' in col0:
            continue
            
        # Check if this is a data row (has CSI Division in col1)
        if col1 and ('Division' in col1 or re.match(r'\d{2}\s*\d{2}', col1)):
            # Extract item name (Arabic with possible English in parentheses)
            item_name_ar = col0
            item_name_en = ""
            
            # Try to extract English name from parentheses
            en_match = re.search(r'\(([^)]+)\)', col0)
            if en_match:
                item_name_en = en_match.group(1)
                item_name_ar = re.sub(r'\s*\([^)]+\)\s*', ' ', col0).strip()
            
            # Generate item key
            item_key = generate_item_key(item_name_ar, current_category_id)
            
            # Parse CSI division
            csi_division = col1
            
            # Parse activities
            activities = extract_activities(col2)
            
            # Parse unit and notes
            unit_notes = col3
            default_unit = extract_unit(unit_notes)
            notes = extract_notes(unit_notes)
            
            item = {
                "item_key": item_key,
                "item_name_ar": item_name_ar,
                "item_name_en": item_name_en if item_name_en else translate_item_name(item_name_ar),
                "category_id": current_category_id,
                "csi_section": csi_division,
                "typical_activities": activities[:5],  # Limit to 5 activities
                "default_unit": default_unit,
                "implementation_notes": notes,
                "synonyms_ar": generate_synonyms_ar(item_name_ar),
                "synonyms_en": generate_synonyms_en(item_name_en if item_name_en else "")
            }
            
            enhanced_items.append(item)
            print(f"    ✅ {item_name_ar[:40]}...")
    
    return enhanced_items

def generate_item_key(name_ar, category_id):
    """Generate a unique item key"""
    # Map common terms to keys
    key_map = {
        'قواعد منفصلة': 'FOOT_ISO',
        'قواعد شريطية': 'FOOT_STRIP',
        'لبشة': 'RAFT',
        'سملات': 'TIE_BEAM',
        'كمرات أرضية': 'TIE_BEAM',
        'أعمدة': 'COLUMN',
        'بلاطة': 'SLAB',
        'بلاطات': 'SLAB',
        'شدة': 'FORMWORK',
        'تسليح': 'REINF',
        'صب': 'CAST',
        'تجريف': 'TOPSOIL',
        'حفر': 'EXCAV',
        'سند': 'SHORING',
        'ردم': 'BACKFILL',
        'تسوية': 'GRADING',
        'نزح سطحي': 'SURF_DRAIN',
        'نزح جوفي': 'DEWATER',
        'تصريف': 'STORM',
        'عزل قواعد': 'WP_FOUND',
        'عزل الحمامات': 'WP_WET',
        'عزل الأسطح': 'WP_ROOF',
        'عزل خزانات': 'WP_TANK',
        'محارة': 'PLASTER',
        'دهانات': 'PAINT',
        'بلاط': 'TILE',
        'رخام': 'STONE',
        'جرانيت': 'STONE',
        'أرضيات خشبية': 'WOOD_FLOOR',
        'باركيه': 'WOOD_FLOOR',
        'أسقف معلقة': 'CEIL_SUSP',
        'أسقف مستعارة': 'CEIL_ACOUS',
        'تمديدات مياه': 'WATER_PIPE',
        'صرف صحي': 'SANITARY',
        'تجهيزات صحية': 'FIXTURES'
    }
    
    prefix = (category_id or 'GEN').upper()[:4]
    
    for ar_term, key_suffix in key_map.items():
        if ar_term in name_ar:
            return f"{prefix}_{key_suffix}"
    
    # Fallback: generate from first few chars
    clean_name = re.sub(r'[^\w\s]', '', name_ar)[:10].upper()
    return f"{prefix}_{clean_name}"

def extract_unit(text):
    """Extract default unit from text"""
    if not text:
        return "m²"
    
    unit_patterns = [
        (r'm[³³]|م³|CUM', 'CUM'),
        (r'm[²²]|م²|SQM', 'SQM'),
        (r'RM|LM|م\.ط', 'RM'),
        (r'KG|TON|طن', 'TON'),
        (r'each|عدد|count', 'EACH'),
        (r'system|نظام', 'SYSTEM'),
        (r'day|يوم', 'DAY')
    ]
    
    for pattern, unit in unit_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return unit
    
    return "SQM"

def extract_notes(text):
    """Extract implementation notes from text"""
    if not text:
        return ""
    # Remove unit mentions and clean up
    notes = re.sub(r'm[²³]|م[²³]|CUM|SQM|RM|LM', '', text)
    notes = re.sub(r'\s*[—–-]\s*', ' - ', notes)
    return notes.strip()[:200]  # Limit length

def translate_item_name(name_ar):
    """Basic translation for common terms"""
    translations = {
        'قواعد منفصلة': 'Isolated Footings',
        'قواعد شريطية': 'Strip Footings',
        'لبشة': 'Raft Foundation',
        'سملات': 'Tie Beams',
        'كمرات أرضية': 'Ground Beams',
        'أعمدة خرسانية': 'Concrete Columns',
        'بلاطة على التربة': 'Slab on Grade',
        'بلاطات أدوار': 'Suspended Slabs',
        'شدة عامة': 'General Formwork',
        'تسليح عامة': 'General Reinforcement',
        'صب وخرسانة': 'Casting & Curing',
        'تجريف': 'Topsoil Stripping',
        'حفر للقواعد': 'Foundation Excavation',
        'سند جوانب الحفر': 'Shoring',
        'ردم ودمك': 'Backfill & Compaction',
        'تسوية': 'Grading',
        'نزح سطحي': 'Surface Drainage',
        'نزح جوفي': 'Dewatering',
        'شبكات تصريف': 'Drainage Networks',
        'عزل قواعد': 'Foundation Waterproofing',
        'عزل الحمامات': 'Wet Area Waterproofing',
        'عزل الأسطح': 'Roof Waterproofing',
        'عزل خزانات': 'Tank Waterproofing',
        'محارة': 'Plastering',
        'دهانات داخلية': 'Interior Painting',
        'بلاط سيراميك': 'Ceramic Tiling',
        'رخام': 'Marble Finishes',
        'جرانيت': 'Granite Finishes',
        'أرضيات خشبية': 'Wood Flooring',
        'أسقف معلقة': 'Suspended Ceilings',
        'أسقف مستعارة': 'Acoustic Ceilings',
        'تمديدات مياه': 'Water Supply Piping',
        'صرف صحي': 'Sanitary Piping',
        'تجهيزات صحية': 'Plumbing Fixtures'
    }
    
    for ar, en in translations.items():
        if ar in name_ar:
            return en
    return name_ar

def generate_synonyms_ar(name_ar):
    """Generate Arabic synonyms"""
    synonyms = [name_ar]
    
    # Add common variations
    if 'قواعد' in name_ar:
        synonyms.extend(['أساسات', 'فوتينج'])
    if 'لبشة' in name_ar:
        synonyms.extend(['حصيرة', 'رافت', 'mat foundation'])
    if 'محارة' in name_ar:
        synonyms.extend(['بياض', 'لياسة', 'plaster'])
    if 'عزل' in name_ar:
        synonyms.append('insulation')
    if 'دهانات' in name_ar:
        synonyms.extend(['بوية', 'طلاء', 'paint'])
    
    return list(set(synonyms))[:5]

def generate_synonyms_en(name_en):
    """Generate English synonyms"""
    synonyms = [name_en.lower()] if name_en else []
    
    name_lower = name_en.lower() if name_en else ""
    
    if 'footing' in name_lower:
        synonyms.extend(['foundation', 'base'])
    if 'raft' in name_lower:
        synonyms.extend(['mat foundation', 'slab foundation'])
    if 'plaster' in name_lower:
        synonyms.extend(['render', 'rendering'])
    if 'waterproof' in name_lower:
        synonyms.extend(['membrane', 'damp proofing'])
    
    return list(set(synonyms))[:5]

def merge_with_existing(new_items):
    """Merge new items with existing database"""
    print("\n📚 Loading existing database...")
    
    try:
        with open(EXISTING_JSON, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {"categories": [], "items": []}
    
    # Create lookup by item_key
    existing_keys = {item.get('item_key', ''): item for item in existing_data.get('items', [])}
    
    # Merge or add new items
    merged_items = []
    updated_count = 0
    new_count = 0
    
    for new_item in new_items:
        key = new_item['item_key']
        if key in existing_keys:
            # Merge: add new fields to existing item
            merged = existing_keys[key].copy()
            merged['typical_activities'] = new_item.get('typical_activities', [])
            merged['implementation_notes'] = new_item.get('implementation_notes', '')
            if 'csi_section' in new_item:
                merged['csi_section'] = new_item['csi_section']
            merged_items.append(merged)
            updated_count += 1
        else:
            merged_items.append(new_item)
            new_count += 1
    
    # Add remaining existing items that weren't updated
    for key, item in existing_keys.items():
        if not any(m['item_key'] == key for m in merged_items):
            merged_items.append(item)
    
    print(f"  ✅ Updated: {updated_count} items")
    print(f"  ➕ New: {new_count} items")
    print(f"  📊 Total: {len(merged_items)} items")
    
    # Build final structure
    final_data = {
        "version": "2.0",
        "last_updated": "2026-01-04",
        "categories": existing_data.get('categories', []),
        "items": merged_items
    }
    
    return final_data

def main():
    print("=" * 60)
    print("🚀 CSI Database Enhancement Tool")
    print("=" * 60)
    
    # Extract data from Excel
    new_items = parse_excel_data()
    print(f"\n📊 Extracted {len(new_items)} items from Excel")
    
    # Merge with existing database
    final_data = merge_with_existing(new_items)
    
    # Save enhanced database
    print(f"\n💾 Saving to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ Enhancement complete!")
    print("=" * 60)
    
    # Print summary
    print("\n📋 Sample enhanced item:")
    if final_data['items']:
        sample = final_data['items'][0]
        print(json.dumps(sample, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
