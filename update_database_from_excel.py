"""
Automatic CSI Database Updater
Reads from CSI.xlsm and updates database/csi_data.db
"""
import pandas as pd
import sqlite3
import os
from datetime import datetime

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def update_database():
    """Main function to update database from Excel"""
    
    print("=" * 100)
    log("CSI DATABASE AUTO-UPDATER")
    print("=" * 100)
    
    # Check if Excel file exists
    excel_file = 'CSI.xlsm'
    if not os.path.exists(excel_file):
        log(f"ERROR: {excel_file} not found!")
        return False
    
    log(f"Reading Excel file: {excel_file}")
    
    try:
        # Read Excel file with proper header
        df = pd.read_excel(excel_file, engine='openpyxl', header=0)
        log(f"Loaded {len(df)} rows from Excel")
        log(f"Columns: {len(df.columns)} columns detected")
        
    except Exception as e:
        log(f"ERROR reading Excel: {e}")
        return False
    
    # Clean up the data
    log("Cleaning data...")
    
    # Remove rows where description is empty (updated column name)
    df = df[df['ITEM DESCRIPTION_Name_Item'].notna()]
    df = df[df['ITEM DESCRIPTION_Name_Item'] != 'ITEM DESCRIPTION_Name_Item']  # Remove duplicate headers
    
    # Remove rows where main division code is not valid (updated column name)
    df = df[df['Code_Main_Division'].notna()]
    
    # Strip whitespace from all string columns
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
    
    # Replace 'nan' strings with None
    df = df.replace('nan', None)
    df = df.replace('', None)
    
    log(f"After cleaning: {len(df)} valid rows")
    
    # Create database path
    DB_PATH = os.path.join('database', 'csi_data.db')
    
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    log(f"Connecting to database: {DB_PATH}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Drop and recreate table
        log("Recreating database table...")
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
        log("Creating database indexes...")
        cursor.execute('CREATE INDEX idx_main_div ON csi_items(main_div_code)')
        cursor.execute('CREATE INDEX idx_sub1 ON csi_items(sub_div1_code)')
        cursor.execute('CREATE INDEX idx_sub2 ON csi_items(sub_div2_code)')
        cursor.execute('CREATE INDEX idx_item ON csi_items(item_code)')
        cursor.execute('CREATE INDEX idx_full_code ON csi_items(full_code)')
        
        # Insert data
        log("Inserting data into database...")
        inserted = 0
        skipped = 0
        
        for idx, row in df.iterrows():
            try:
                # Get base info (updated column names)
                full_code = row.get('CSI CODE(full Code)')
                main_code = row.get('Code_Main_Division')
                main_name = row.get('Name_Main_Division')
                sub1_code = row.get('Sub_Division1_Code')
                
                # Fix invalid Sub-Division 1 Codes (data cleaning)
                if not sub1_code or str(sub1_code).strip() in ['0', '-', 'nan', 'None']:
                    # Try to infer from Sub-Division 2
                    raw_sub2 = str(row.get('Sub_Division2_Code', ''))
                    raw_full = str(row.get('CSI CODE(full Code)', ''))
                    
                    if len(raw_sub2) >= 3 and raw_sub2[:3].isdigit():
                         sub1_code = raw_sub2[:3]
                    elif len(raw_full) >= 3 and raw_full[:3].isdigit():
                         sub1_code = raw_full[:3]
                
                sub1_name = row.get('Sub_Division1_Name')
                sub2_code = row.get('Sub_Division2_Code')
                sub2_name = row.get('Sub_Division2_Name_2')
                item_code = row.get('ITEM DESCRIPTION_Code_Item')
                description = row.get('ITEM DESCRIPTION_Name_Item')
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
                
                # Get crew details (updated column names)
                crew_data = []
                # First crew member has different naming pattern
                crew_num = row.get('Crew_Number1')
                crew_desc = row.get('Crew_Memeber_ Desc.1')
                crew_num = str(crew_num) if pd.notna(crew_num) and str(crew_num) != 'nan' else None
                crew_desc = str(crew_desc) if pd.notna(crew_desc) and str(crew_desc) != 'nan' else None
                crew_data.extend([crew_num, crew_desc])
                
                # Remaining crew members
                for i in range(2, 14):
                    crew_num = row.get(f'Crew_Memeber_ Number{i}')
                    crew_desc = row.get(f'Crew_Memeber_ Desc.{i}')
                    
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
                    log(f"Progress: {inserted} rows inserted...")
                    
            except Exception as e:
                log(f"Warning at row {idx}: {e}")
                skipped += 1
                continue
        
        # Commit changes
        conn.commit()
        
        print("=" * 100)
        log("DATABASE UPDATE COMPLETE!")
        print("=" * 100)
        log(f"[OK] Rows inserted: {inserted}")
        log(f"[SKIP] Rows skipped: {skipped}")
        
        # Quick verification
        cursor.execute("SELECT COUNT(DISTINCT main_div_code) FROM csi_items")
        div_count = cursor.fetchone()[0]
        log(f"[OK] Main Divisions: {div_count}")
        
        cursor.execute("SELECT COUNT(*) FROM csi_items WHERE daily_output IS NOT NULL")
        productivity_count = cursor.fetchone()[0]
        log(f"[OK] Items with productivity data: {productivity_count}")
        
        conn.close()
        
        print("=" * 100)
        log("SUCCESS: Database updated from CSI.xlsm")
        log("You can now restart the Flask server to use the new data")
        print("=" * 100)
        
        return True
        
    except Exception as e:
        log(f"ERROR updating database: {e}")
        return False

if __name__ == "__main__":
    success = update_database()
    
    print("\n" + "=" * 100)
    if success:
        print("STATUS: [OK] Update completed successfully!")
    else:
        print("STATUS: [FAILED] Update failed - please check the errors above")
    print("=" * 100)
    
    input("\nPress Enter to exit...")
