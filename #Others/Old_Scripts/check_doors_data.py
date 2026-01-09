import pandas as pd

# Read Excel file
df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=None)

print("="*100)
print("SEARCHING FOR WOOD AND DOORS ENTRIES")
print("="*100)

# Find all rows mentioning WOOD or DOOR
for idx in range(len(df)):
    row_text = ' '.join([str(x) for x in df.iloc[idx, :10].values if pd.notna(x)])
    
    if 'WOOD' in row_text.upper() or 'DOOR' in row_text.upper():
        print(f"\n{'='*100}")
        print(f"ROW {idx}:")
        print(f"{'='*100}")
        
        # Show this row and surrounding rows for context
        for offset in range(-2, 5):
            row_num = idx + offset
            if 0 <= row_num < len(df):
                marker = ">>> " if offset == 0 else "    "
                col_data = [str(df.iloc[row_num, i])[:40] if pd.notna(df.iloc[row_num, i]) else 'NaN' for i in range(10)]
                print(f"{marker}Row {row_num:4d}: Col0='{col_data[0]}' | Col1='{col_data[1]}' | Col2='{col_data[2]}' | Col3='{col_data[3]}' | Col4='{col_data[4]}' | Col5='{col_data[5]}' | Col6='{col_data[6]}'")
        
        if idx > 500:  # Limit to avoid too much output
            break

print("\n" + "="*100)
print("EXAMINING DOOR/WOOD DIVISION STRUCTURE")
print("="*100)

# Find Division 08 specifically (likely DOORS)
for idx in range(len(df)):
    col0 = str(df.iloc[idx, 0]) if pd.notna(df.iloc[idx, 0]) else ""
    
    if col0.startswith('Division 08') or col0.startswith('08'):
        print(f"\nFound Division 08 at row {idx}:")
        # Show next 30 rows
        for i in range(30):
            row_num = idx + i
            if row_num < len(df):
                print(f"  Row {row_num:4d}: {[str(df.iloc[row_num, j])[:35] for j in range(8)]}")
        break

print("\n" + "="*100)
print("CHECKING CURRENT DATABASE FOR DOORS")
print("="*100)

import sqlite3
conn = sqlite3.connect('database/csi_data.db')
cursor = conn.cursor()

# Check what's in database for doors
cursor.execute("""
    SELECT main_div_code, main_div_name, sub_div1_code, sub_div1_name, 
           sub_div2_code, sub_div2_name, description
    FROM csi_items 
    WHERE main_div_name LIKE '%DOOR%' OR main_div_name LIKE '%WOOD%'
    LIMIT 10
""")

print("\nDoors/Wood in database:")
for row in cursor.fetchall():
    print(f"  Main: {row[0]} - {row[1]}")
    print(f"  Sub1: {row[2]} - {row[3]}")
    print(f"  Sub2: {row[4]} - {row[5]}")
    print(f"  Item: {row[6][:60]}")
    print()

conn.close()
