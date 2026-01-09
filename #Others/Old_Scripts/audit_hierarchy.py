"""
Comprehensive audit script to compare Excel hierarchy with Database
"""
import pandas as pd
import sqlite3

print("="*100)
print("CSI DATA HIERARCHY AUDIT")
print("="*100)

# Read Excel with header at row 1 (0-indexed)
df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)

print(f"\nTotal rows in Excel: {len(df)}")

# Clean up data
df = df[df['Code_Main'].notna()]
df = df[df['Code_Main'] != 'Code_Main']  # Remove duplicate headers

# Convert to strings and strip
for col in ['Code_Main', 'Name_Main', 'Code_1', 'Name_1', 'Code_2', 'Name_2']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace('nan', '')
        df[col] = df[col].replace('None', '')

print("\n" + "="*100)
print("EXCEL STRUCTURE ANALYSIS")
print("="*100)

# Get unique Main Divisions from Excel
excel_main_divs = df[['Code_Main', 'Name_Main']].drop_duplicates()
excel_main_divs = excel_main_divs[excel_main_divs['Code_Main'] != '']
print(f"\nMain Divisions in Excel: {len(excel_main_divs)}")

for _, row in excel_main_divs.iterrows():
    code = row['Code_Main']
    name = row['Name_Main']
    
    # Get Sub-Division 1 for this Main Division
    sub1_df = df[df['Code_Main'] == code][['Code_1', 'Name_1']].drop_duplicates()
    sub1_df = sub1_df[(sub1_df['Code_1'] != '') & (sub1_df['Name_1'] != '')]
    
    print(f"\n{'='*80}")
    print(f"Division {code}: {name}")
    print(f"{'='*80}")
    print(f"  Sub-Division 1 count: {len(sub1_df)}")
    
    for _, sub1_row in sub1_df.iterrows():
        sub1_code = sub1_row['Code_1']
        sub1_name = sub1_row['Name_1']
        
        # Get Sub-Division 2 count for this Sub1
        sub2_df = df[(df['Code_Main'] == code) & (df['Code_1'] == sub1_code)][['Code_2', 'Name_2']].drop_duplicates()
        sub2_df = sub2_df[(sub2_df['Code_2'] != '') & (sub2_df['Name_2'] != '')]
        
        print(f"    Sub1 '{sub1_code}' - {sub1_name[:50]}: {len(sub2_df)} Sub-Division 2 entries")

# Now compare with Database
print("\n" + "="*100)
print("DATABASE COMPARISON")
print("="*100)

conn = sqlite3.connect('database/csi_data.db')
cursor = conn.cursor()

# Get database Main Divisions
cursor.execute("SELECT DISTINCT main_div_code, main_div_name FROM csi_items ORDER BY main_div_code")
db_main_divs = cursor.fetchall()
print(f"\nMain Divisions in DB: {len(db_main_divs)}")

discrepancies = []

for main_code, main_name in db_main_divs:
    # Get DB Sub1 count
    cursor.execute("""
        SELECT DISTINCT sub_div1_code, sub_div1_name 
        FROM csi_items 
        WHERE main_div_code = ? AND sub_div1_code IS NOT NULL AND sub_div1_code != ''
        ORDER BY sub_div1_code
    """, (main_code,))
    db_sub1 = cursor.fetchall()
    
    # Get Excel Sub1 count
    excel_sub1 = df[df['Code_Main'] == main_code][['Code_1', 'Name_1']].drop_duplicates()
    excel_sub1 = excel_sub1[(excel_sub1['Code_1'] != '') & (excel_sub1['Name_1'] != '')]
    
    if len(db_sub1) != len(excel_sub1):
        discrepancies.append({
            'division': f"{main_code} - {main_name}",
            'excel_count': len(excel_sub1),
            'db_count': len(db_sub1)
        })
    
    print(f"\nDivision {main_code} - {main_name}")
    print(f"  Excel Sub1: {len(excel_sub1)} | DB Sub1: {len(db_sub1)}")
    
    # Show details
    print(f"  Excel Sub-Divisions 1:")
    for _, row in excel_sub1.iterrows():
        print(f"    - {row['Code_1']}: {row['Name_1'][:60]}")
    
    print(f"  Database Sub-Divisions 1:")
    for sub1_code, sub1_name in db_sub1:
        print(f"    - {sub1_code}: {sub1_name[:60] if sub1_name else 'N/A'}")

print("\n" + "="*100)
print("DISCREPANCY SUMMARY")
print("="*100)

if discrepancies:
    print("\n[WARNING] FOUND DISCREPANCIES:")
    for d in discrepancies:
        print(f"  {d['division']}: Excel={d['excel_count']}, DB={d['db_count']}")
else:
    print("\n[OK] No discrepancies found in Sub-Division 1 counts")

# Check Division 08 specifically
print("\n" + "="*100)
print("DIVISION 08 (DOORS & WINDOWS) DETAILED CHECK")
print("="*100)

# Excel
excel_div08 = df[df['Code_Main'] == '08']
excel_sub1_08 = excel_div08[['Code_1', 'Name_1']].drop_duplicates()
excel_sub1_08 = excel_sub1_08[(excel_sub1_08['Code_1'] != '') & (excel_sub1_08['Name_1'] != '')]

print("\nIn Excel:")
for _, row in excel_sub1_08.iterrows():
    print(f"  Sub1 Code='{row['Code_1']}' Name='{row['Name_1']}'")

# Database
cursor.execute("""
    SELECT DISTINCT sub_div1_code, sub_div1_name 
    FROM csi_items 
    WHERE main_div_code = '08'
    ORDER BY sub_div1_code
""")
db_sub1_08 = cursor.fetchall()

print("\nIn Database:")
for code, name in db_sub1_08:
    print(f"  Sub1 Code='{code}' Name='{name}'")

conn.close()

print("\n" + "="*100)
print("AUDIT COMPLETE")
print("="*100)
