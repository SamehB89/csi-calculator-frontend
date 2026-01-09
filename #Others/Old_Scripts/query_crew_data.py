import sqlite3

conn = sqlite3.connect('d:/SUPERMANn/CSI_Project/database/csi_data.db')
cursor = conn.cursor()

# Search for concrete related items
print("="*80)
print("SEARCHING FOR CONCRETE FOUNDATION/MAT ITEMS:")
print("="*80)

cursor.execute("""
    SELECT full_code, description, unit, daily_output, man_hours, equip_hours, 
           crew_structure, crew_num_1, crew_desc_1, crew_num_2, crew_desc_2
    FROM csi_items 
    WHERE (description LIKE '%CONCRETE%' AND (description LIKE '%MAT%' OR description LIKE '%RAFT%' OR description LIKE '%FOUNDATION%'))
    OR (description LIKE '%REINFORCED%' AND description LIKE '%SLAB%')
    LIMIT 20
""")

rows = cursor.fetchall()
print(f"\nFound {len(rows)} items:\n")

for row in rows:
    print(f"Code: {row[0]}")
    print(f"Description: {row[1]}")
    print(f"Unit: {row[2]}")
    print(f"Daily Output: {row[3]}")
    print(f"Man Hours: {row[4]}")
    print(f"Equip Hours: {row[5]}")
    print(f"Crew Structure: {row[6]}")
    if row[7]:
        print(f"  Crew 1: {row[7]} {row[8]}")
    if row[9]:
        print(f"  Crew 2: {row[9]} {row[10]}")
    print("-"*80)

print("\n" + "="*80)
print("SEARCHING FOR DIVISION 03 - CONCRETE ITEMS:")
print("="*80)

cursor.execute("""
    SELECT full_code, description, unit, daily_output, man_hours, crew_structure
    FROM csi_items 
    WHERE main_div_code = '03'
    AND description LIKE '%CONCRETE%'
    LIMIT 15
""")

rows2 = cursor.fetchall()
print(f"\nFound {len(rows2)} concrete items:\n")

for row in rows2:
    print(f"{row[0]} | {row[1][:60]} | Unit:{row[2]} | Output:{row[3]} | ManHrs:{row[4]}")

conn.close()
print("\n" + "="*80)
print("Query completed!")
