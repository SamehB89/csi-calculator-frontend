"""
Improved CSI data import with correct hierarchy tracking
"""
import pandas as pd
import sqlite3
import os

# Read Excel file with proper header
print("="*100)
print("IMPROVED CSI DATA IMPORT")
print("="*100)

df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)

print(f"\nTotal rows loaded: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Clean up the data
print("\nCleaning data...")

# Remove rows where description is empty
df = df[df['Name_Item'].notna()]
df = df[df['Name_Item'] != 'Name_Item']  # Remove duplicate headers

# Remove rows where main division code is not valid
df = df[df['Code_Main'].notna()]

# Strip whitespace from all string columns
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str).str.strip()

# Replace 'nan' strings with None
df = df.replace('nan', None)
df = df.replace('', None)

print(f"After cleaning: {len(df)} rows")

# Create database
DB_PATH = os.path.join('database', 'csi_data.db')
print(f"\nConnecting to database: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop and recreate table
print("Recreating table...")
cursor.execute('DROP TABLE IF EXISTS csi_items')

cursor.execute('''
CREATE TABLE csi_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_code TEXT,
    main_div_code TEXT,
    main_div_name TEXT,
    sub_div1_code TEXT,
    sub_div1_name TEXT,
    sub_div2_code TEXT,
    sub_div2_name TEXT,
    item_code TEXT,
    description TEXT,
    unit TEXT,
    daily_output REAL,
    man_hours REAL,
    equip_hours REAL,
    crew_structure TEXT,
    crew_num_1 TEXT,
    crew_desc_1 TEXT,
    crew_num_2 TEXT,
    crew_desc_2 TEXT,
    crew_num_3 TEXT,
    crew_desc_3 TEXT,
    crew_num_4 TEXT,
    crew_desc_4 TEXT,
    crew_num_5 TEXT,
    crew_desc_5 TEXT,
    crew_num_6 TEXT,
    crew_desc_6 TEXT,
    crew_num_7 TEXT,
    crew_desc_7 TEXT,
    crew_num_8 TEXT,
    crew_desc_8 TEXT,
    crew_num_9 TEXT,
    crew_desc_9 TEXT,
    crew_num_10 TEXT,
    crew_desc_10 TEXT,
    crew_num_11 TEXT,
    crew_desc_11 TEXT,
    crew_num_12 TEXT,
    crew_desc_12 TEXT,
    crew_num_13 TEXT,
    crew_desc_13 TEXT
)
''')

# Create indexes for faster querying
print("Creating indexes...")
cursor.execute('CREATE INDEX idx_main_div ON csi_items(main_div_code)')
cursor.execute('CREATE INDEX idx_sub1 ON csi_items(sub_div1_code)')
cursor.execute('CREATE INDEX idx_sub2 ON csi_items(sub_div2_code)')
cursor.execute('CREATE INDEX idx_item ON csi_items(item_code)')

# Insert data with proper hierarchy tracking
print("\nInserting data...")
inserted = 0
skipped = 0

for idx, row in df.iterrows():
    try:
        # Get base info
        full_code = row.get('CSI CODE(full Code)')
        main_code = row.get('Code_Main')
        main_name = row.get('Name_Main')
        sub1_code = row.get('Code_1')
        sub1_name = row.get('Name_1')
        sub2_code = row.get('Code_2')
        sub2_name = row.get('Name_2')
        item_code = row.get('Code_Item')
        description = row.get('Name_Item')
        unit = row.get('UNIT')
        
        # Skip if essential fields are missing
        if not description or description == 'nan':
            skipped += 1
            continue
        
        # Get productivity data
        daily_output = row.get('DAILY OUTPUT')
        man_hours = row.get('MAN HOURS')
        equip_hours = row.get('EQUIP. HOURS')
        crew_structure = row.get('CREW STRUCTURE COMBINED')
        
        # Convert to proper types
        daily_output = float(daily_output) if pd.notna(daily_output) else None
        man_hours = float(man_hours) if pd.notna(man_hours) else None
        equip_hours = float(equip_hours) if pd.notna(equip_hours) else None
        
        # Get crew details
        crew_data = []
        for i in range(1, 14):
            crew_num = row.get(f'Crew Number{i}')
            crew_desc = row.get(f'Crew Desc.{i}')
            
            crew_num = str(crew_num) if pd.notna(crew_num) and str(crew_num) != 'nan' else None
            crew_desc = str(crew_desc) if pd.notna(crew_desc) and str(crew_desc) != 'nan' else None
            
            crew_data.extend([crew_num, crew_desc])
        
        # Insert into database
        cursor.execute('''
            INSERT INTO csi_items (
                full_code, main_div_code, main_div_name,
                sub_div1_code, sub_div1_name,
                sub_div2_code, sub_div2_name,
                item_code, description, unit,
                daily_output, man_hours, equip_hours, crew_structure,
                crew_num_1, crew_desc_1, crew_num_2, crew_desc_2,
                crew_num_3, crew_desc_3, crew_num_4, crew_desc_4,
                crew_num_5, crew_desc_5, crew_num_6, crew_desc_6,
                crew_num_7, crew_desc_7, crew_num_8, crew_desc_8,
                crew_num_9, crew_desc_9, crew_num_10, crew_desc_10,
                crew_num_11, crew_desc_11, crew_num_12, crew_desc_12,
                crew_num_13, crew_desc_13
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [
            full_code, main_code, main_name,
            sub1_code, sub1_name,
            sub2_code, sub2_name,
            item_code, description, unit,
            daily_output, man_hours, equip_hours, crew_structure
        ] + crew_data)
        
        inserted += 1
        if inserted % 500 == 0:
            print(f"  Inserted {inserted} rows...")
            
    except Exception as e:
        print(f"Error at row {idx}: {e}")
        skipped += 1
        continue

# Commit changes
conn.commit()

print(f"\n{'='*100}")
print(f"IMPORT COMPLETE")
print(f"{'='*100}")
print(f"Rows inserted: {inserted}")
print(f"Rows skipped: {skipped}")

# Verify the data
print(f"\n{'='*100}")
print("VERIFICATION - Sample Data")
print(f"{'='*100}")

cursor.execute("""
    SELECT DISTINCT main_div_code, main_div_name
    FROM csi_items
    ORDER BY main_div_code
""")
print("\nMain Divisions:")
for row in cursor.fetchall():
    print(f"  {row[0]:3s} - {row[1]}")

# Check Division 06 (WOOD & PLASTICS) structure
print(f"\n{'='*100}")
print("Division 06 (WOOD & PLASTICS) Structure:")
print(f"{'='*100}")

cursor.execute("""
    SELECT DISTINCT sub_div1_code, sub_div1_name
    FROM csi_items
    WHERE main_div_code = '06'
    ORDER BY sub_div1_code
""")
print("\nSub-Divisions 1:")
for row in cursor.fetchall():
    print(f"  {row[0]:10s} - {row[1]}")

cursor.execute("""
    SELECT DISTINCT sub_div2_code, sub_div2_name
    FROM csi_items
    WHERE main_div_code = '06' AND sub_div1_code = '1'
    ORDER BY sub_div2_code
""")
print("\nSub-Divisions 2 (under sub1='1'):")
count = 0
for row in cursor.fetchall():
    if row[0]:
        print(f"  {row[0]:15s} - {row[1]}")
        count += 1
        if count > 15:
            print("  ... and more")
            break

# Check Division 08 (DOORS & WINDOWS) structure  
print(f"\n{'='*100}")
print("Division 08 (DOORS & WINDOWS) Structure:")
print(f"{'='*100}")

cursor.execute("""
    SELECT DISTINCT sub_div1_code, sub_div1_name
    FROM csi_items
    WHERE main_div_code = '08'
    ORDER BY sub_div1_code
""")
print("\nSub-Divisions 1:")
for row in cursor.fetchall():
    if row[0]:
        print(f"  {row[0]:10s} - {row[1]}")

conn.close()

print(f"\n{'='*100}")
print("Database updated successfully!")
print("Restart the Flask server to use the new data.")
print(f"{'='*100}")
