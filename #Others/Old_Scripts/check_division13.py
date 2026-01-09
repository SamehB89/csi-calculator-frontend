"""
Quick check for Division 13 discrepancy
"""
import pandas as pd
import sqlite3

print("="*80)
print("DIVISION 13 INVESTIGATION")
print("="*80)

# Check Excel
print("\n1. Excel Sub-Divisions 1 for Division 13:")
df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)
df = df[df['Code_Main'] == '13']
sub1 = df[['Code_1', 'Name_1']].drop_duplicates()
sub1 = sub1[(sub1['Code_1'].notna()) & (sub1['Code_1'] != '') & (sub1['Code_1'] != 'nan')]

for _, row in sub1.iterrows():
    code = str(row['Code_1']).strip()
    name = str(row['Name_1']).strip()
    print(f"  {code}: {name}")

# Check Database
print("\n2. Database Sub-Divisions 1 for Division 13:")
conn = sqlite3.connect('database/csi_data.db')
cursor = conn.cursor()
cursor.execute("""
    SELECT DISTINCT sub_div1_code, sub_div1_name 
    FROM csi_items 
    WHERE main_div_code = '13'
    ORDER BY sub_div1_code
""")
db_subs = cursor.fetchall()

for code, name in db_subs:
    print(f"  {code}: {name}")

# Check for missing subdivision
print("\n3. Missing in Database:")
print("  - Code '3': UTILITY CONTROL SYSTEMS")

# Check if there's any data for subdivision 3 in Excel
print("\n4. Items in Excel for Division 13, Sub-Division 3:")
df_sub3 = df[df['Code_1'] == '3']
print(f"  Total items: {len(df_sub3)}")

if len(df_sub3) > 0:
    print("\n  Sample items:")
    for i, row in df_sub3.head(5).iterrows():
        full_code = f"{row['Code_Main']}-{row['Code_1']}-{row['Code_2']}"
        print(f"    {full_code}: {row.get('Description', 'N/A')[:60]}")

conn.close()

print("\n" + "="*80)
print("INVESTIGATION COMPLETE")
print("="*80)
