"""
Test CSI Lookup Integration
"""
import sys
sys.path.insert(0, r'd:\SUPERMANn\CSI_Project\backend')

from intelligent_ai import preprocess_query_with_csi

# Test queries
test_queries = [
    ("لبشة 200 متر مكعب", 'ar'),
    ("isolated footings 50 m3", 'en'),
    ("محارة حوائط 100 متر مربع", 'ar'),
    ("plaster", 'en'),
    ("عزل أسطح", 'ar'),
    ("waterproofing roof", 'en'),
    ("بلاط سيراميك", 'ar'),
    ("ceramic tiles 80 sqm", 'en'),
]

print("=" * 70)
print("🧪 TESTING CSI LOOKUP INTEGRATION")
print("=" * 70)

for query, lang in test_queries:
    print(f"\n📝 Query: '{query}' (lang={lang})")
    print("-" * 70)
    
    result = preprocess_query_with_csi(query, lang)
    
    if result['has_matches']:
        print(f"✅ Found {len(result['csi_matches'])} matches")
        
        if result['query_quantity']:
            print(f"   Quantity detected: {result['query_quantity']}")
        
        print(f"\n   Best Match:")
        best = result['best_match']
        print(f"   ├─ Item: {best['item_name_ar']} ({best['item_name_en']})")
        print(f"   ├─ CSI: {best['csi_section']}")
        print(f"   ├─ Division: {best['csi_division']}")
        print(f"   ├─ Unit: {best['default_unit']}")
        print(f"   ├─ Confidence: {best['match_confidence']}%")
        print(f"   └─ Activities: {', '.join(best['typical_activities'][:2])}...")
        
        if len(result['csi_matches']) > 1:
            print(f"\n   Other matches:")
            for match in result['csi_matches'][1:3]:
                print(f"   • {match['item_name_ar']} ({match['match_confidence']}%)")
    else:
        print("❌ No CSI matches found")

print("\n" + "=" * 70)
print("✨ Testing Complete!")
print("=" * 70)
