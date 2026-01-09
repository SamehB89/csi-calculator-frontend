import sqlite3
import pandas as pd
import sys

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 80)
print("CSI DATA QUALITY CHECK")
print("=" * 80)

conn = sqlite3.connect('database/csi_data.db')

# 0. Check table schema
print("\n0. DATABASE SCHEMA:")
print("-" * 80)
schema = pd.read_sql_query("PRAGMA table_info(csi_items)", conn)
print(f"Total Columns: {len(schema)}")
print(schema[['name', 'type']])

# 1. Check for duplicate divisions
print("\n1. CHECKING FOR DUPLICATE MAIN DIVISIONS:")
print("-" * 80)
df = pd.read_sql_query('''
    SELECT main_div_name, COUNT(DISTINCT main_div_code) as code_count, COUNT(*) as item_count
    FROM csi_items
    GROUP BY main_div_name
    ORDER BY code_count DESC, item_count DESC
''', conn)
print(df.head(20))
print(f"\nTOTAL UNIQUE MAIN DIVISIONS: {len(df)}")

# 2. Check for NA entries
print("\n2. CHECKING FOR 'NA' ENTRIES:")
print("-" * 80)
na_check = pd.read_sql_query('''
    SELECT 
        SUM(CASE WHEN main_div_name = 'NA' OR main_div_name IS NULL THEN 1 ELSE 0 END) as main_na,
        SUM(CASE WHEN sub_div1_name = 'NA' OR sub_div1_name IS NULL THEN 1 ELSE 0 END) as sub1_na,
        SUM(CASE WHEN sub_div2_name = 'NA' OR sub_div2_name IS NULL THEN 1 ELSE 0 END) as sub2_na,
        SUM(CASE WHEN description = 'NA' OR description IS NULL THEN 1 ELSE 0 END) as desc_na,
        SUM(CASE WHEN unit = 'NA' OR unit IS NULL THEN 1 ELSE 0 END) as unit_na,
        COUNT(*) as total_items
    FROM csi_items
''', conn)
print(na_check)

# 3. Check for clustered sub-division data in code column
print("\n3. CHECKING FOR UNUSUAL CODES (Clustered data):")
print("-" * 80)
unusual = pd.read_sql_query('''
    SELECT full_code, main_div_name, sub_div1_name, description
    FROM csi_items
    WHERE LENGTH(full_code) > 20 OR full_code LIKE '%:%'
    LIMIT 15
''', conn)
if len(unusual) > 0:
    print(unusual)
    print(f"\nWARNING: FOUND {len(unusual)} items with clustered/unusual codes!")
else:
    print("OK: No clustered/unusual codes found!")

# 4. Sample productivity data
print("\n4. SAMPLE PRODUCTIVITY DATA:")
print("-" * 80)
sample = pd.read_sql_query('''
    SELECT full_code, description, unit, daily_output, man_hours, crew_structure
    FROM csi_items
    WHERE daily_output IS NOT NULL AND daily_output > 0
    LIMIT 10
''', conn)
print(sample)

# 5. Check items with missing productivity data
print("\n5. ITEMS WITH MISSING PRODUCTIVITY DATA:")
print("-" * 80)
missing = pd.read_sql_query('''
    SELECT 
        COUNT(*) as total_items,
        SUM(CASE WHEN daily_output IS NULL OR daily_output = 0 THEN 1 ELSE 0 END) as missing_output,
        ROUND(100.0 * SUM(CASE WHEN daily_output IS NULL OR daily_output = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as missing_percentage,
        SUM(CASE WHEN crew_structure IS NULL OR crew_structure = '' THEN 1 ELSE 0 END) as missing_crew
    FROM csi_items
''', conn)
print(missing)
if missing['missing_percentage'].iloc[0] > 10:
    print(f"\nWARNING: {missing['missing_percentage'].iloc[0]}% of items missing productivity data!")

# 6. Check specific example - Foundation items
print("\n6. FOUNDATION RELATED ITEMS (for crew calculator):")
print("-" * 80)
foundation = pd.read_sql_query('''
    SELECT full_code, description, unit, daily_output, man_hours
    FROM csi_items
    WHERE LOWER(description) LIKE '%foundation%' 
       OR LOWER(description) LIKE '%footing%'
    LIMIT 15
''', conn)
print(foundation)

# 7. Check for duplicate item codes
print("\n7. CHECKING FOR DUPLICATE ITEM CODES:")
print("-" * 80)
duplicates = pd.read_sql_query('''
    SELECT full_code, COUNT(*) as count
    FROM csi_items
    GROUP BY full_code
    HAVING COUNT(*) > 1
    LIMIT 10
''', conn)
if len(duplicates) > 0:
    print(duplicates)
    print(f"\nWARNING: FOUND duplicate item codes!")
    # Show details of one duplicate
    dup_example = pd.read_sql_query(f'''
        SELECT full_code, description, unit, daily_output
        FROM csi_items
        WHERE full_code = '{duplicates.iloc[0]['full_code']}'
    ''', conn)
    print("\nExample of duplicate:")
    print(dup_example)
else:
    print("OK: No duplicate item codes found!")

# 8. Check crew calculator functionality - Concrete items
print("\n8. CONCRETE POUR ITEMS (for crew calculator):")
print("-" * 80)
concrete = pd.read_sql_query('''
    SELECT full_code, description, unit, daily_output, man_hours, crew_structure
    FROM csi_items
    WHERE (LOWER(description) LIKE '%concrete%' AND LOWER(description) LIKE '%pour%')
       OR LOWER(description) LIKE '%placing concrete%'
    LIMIT 10
''', conn)
print(concrete)

conn.close()

print("\n" + "=" * 80)
print("DATA QUALITY CHECK COMPLETED")
print("=" * 80)
print("\nSUMMARY:")
print(f"- Total Items: {na_check['total_items'].iloc[0]}")
print(f"- Items with missing unit: {na_check['unit_na'].iloc[0]}")
print(f"- Items with missing productivity: {missing['missing_output'].iloc[0]} ({missing['missing_percentage'].iloc[0]}%)")
print(f"- Unusual codes found: {len(unusual)}")
