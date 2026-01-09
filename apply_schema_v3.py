import sqlite3
import os

DB_PATH = os.path.join('database', 'csi_data.db')
SCHEMA_PATH = os.path.join('database', 'schema_v3.sql')

def apply_schema():
    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Reading schema from {SCHEMA_PATH}...")
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        
    print("Executing SQL...")
    cursor.executescript(schema_sql)
    
    # Verify
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assemblies'")
    if cursor.fetchone():
        print("SUCCESS: 'assemblies' table created.")
    else:
        print("ERROR: 'assemblies' table NOT created.")

    # Link Components (Need to find valid CSI Codes from existing DB first to be safe)
    # Let's find some standard codes for Forms, Steel, Concrete
    
    # 1. Forms (Look for '03 11' or similar)
    print("Searching for component codes...")
    forms = cursor.execute("SELECT full_code, description FROM csi_items WHERE full_code LIKE '03 11%' OR description LIKE '%Form%' LIMIT 1").fetchone()
    steel = cursor.execute("SELECT full_code, description FROM csi_items WHERE full_code LIKE '03 20%' OR description LIKE '%Reinforc%' LIMIT 1").fetchone()
    pouring = cursor.execute("SELECT full_code, description FROM csi_items WHERE full_code LIKE '03 30%' OR description LIKE '%Pour%' LIMIT 1").fetchone()
    
    assembly_id = cursor.execute("SELECT id FROM assemblies WHERE name_en='Reinforced Concrete Footings'").fetchone()[0]
    
    components = []
    if forms:
        components.append((assembly_id, forms[0], 12.0, 'area', 'Formwork', 'نجارة القواعد'))
        print(f"Found Forms: {forms[0]}")
    if steel:
        components.append((assembly_id, steel[0], 100.0, 'weight', 'Reinforcement', 'حدادة القواعد'))
        print(f"Found Steel: {steel[0]}")
    if pouring:
        components.append((assembly_id, pouring[0], 1.0, 'volume', 'Pouring Concrete', 'صب الخرسانة'))
        print(f"Found Pouring: {pouring[0]}")
        
    print(f"Inserting {len(components)} components...")
    cursor.executemany('''
        INSERT INTO assembly_components (assembly_id, csi_full_code, ratio_to_primary, ratio_type, component_role_en, component_role_ar)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', components)
    
    conn.commit()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    apply_schema()
