"""
Update SQLite database from CSI_latest.csv with proper column mapping
"""
import pandas as pd
import sqlite3
import os

# Paths
CSV_FILE = 'CSI_latest.csv'
DB_PATH = os.path.join('database', 'csi_data.db')

print("="*80)
print("UPDATING DATABASE FROM CSV")
print("="*80)

# Read CSV
print("\nReading CSI_latest.csv...")
df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)

print(f"Loaded {len(df)} rows")

# Clean data - remove header rows that might still be in data
df = df[df['Code_Main'].notna()]
df = df[df['Code_Main'] != 'Code_Main']  # Remove duplicate header rows

print(f"After cleaning: {len(df)} rows")

# Create database connection
print(f"\nConnecting to database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop existing table if exists
print("Dropping existing table...")
cursor.execute('DROP TABLE IF EXISTS csi_items')

# Create new table with proper schema
print("Creating new table...")
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

# Insert data
print("Inserting data...")
inserted = 0
for idx, row in df.iterrows():
    try:
        # Map columns from Excel to database
        full_code = str(row.get('CSI CODE(full Code)', '')).strip()
        main_div_code = str(row.get('Code_Main', '')).strip()
        main_div_name = str(row.get('Name_Main', '')).strip()
        sub_div1_code = str(row.get('Code_1', '')).strip()
        sub_div1_name = str(row.get('Name_1', '')).strip()
        sub_div2_code = str(row.get('Code_2', '')).strip()
        sub_div2_name = str(row.get('Name_2', '')).strip()
        item_code = str(row.get('Code_Item', '')).strip()
        description = str(row.get('Name_Item', '')).strip()
        unit = str(row.get('UNIT', '')).strip()
        
        # Skip if description is empty or nan
        if not description or description == 'nan':
            continue
            
        # Get numeric values
        daily_output = row.get('DAILY OUTPUT', None)
        man_hours = row.get('MAN HOURS', None)
        equip_hours = row.get('EQUIP. HOURS', None)
        crew_structure = str(row.get('CREW STRUCTURE COMBINED', '')).strip()
        
        # Convert to proper types
        daily_output = float(daily_output) if pd.notna(daily_output) else None
        man_hours = float(man_hours) if pd.notna(man_hours) else None
        equip_hours = float(equip_hours) if pd.notna(equip_hours) else None
        
        # Get crew details (1-13)
        crew_data = []
        for i in range(1, 14):
            crew_num = row.get(f'Crew Number{i}', '')
            crew_desc = row.get(f'Crew Desc.{i}', '')
            crew_data.extend([
                str(crew_num).strip() if pd.notna(crew_num) else None,
                str(crew_desc).strip() if pd.notna(crew_desc) else None
            ])
        
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
            full_code, main_div_code, main_div_name,
            sub_div1_code, sub_div1_name,
            sub_div2_code, sub_div2_name,
            item_code, description, unit,
            daily_output, man_hours, equip_hours, crew_structure
        ] + crew_data)
        
        inserted += 1
        if inserted % 500 == 0:
            print(f"  Inserted {inserted} rows...")
            
    except Exception as e:
        print(f"Error inserting row {idx}: {e}")
        continue

# Commit and close
conn.commit()
conn.close()

print(f"\n{'='*80}")
print(f"DATABASE UPDATE COMPLETE")
print(f"{'='*80}")
print(f"Total rows inserted: {inserted}")
print("Database ready for API usage!")
