"""
CSI Data Cleaning Script
========================
This script cleans the CSI data by:
1. Removing division header rows (rows without productivity data)
2. Properly parsing and separating codes
3. Handling NA values
4. Creating a clean CSV for re-import
"""

import pandas as pd
import sqlite3
import os

# Paths
DB_PATH = 'd:/SUPERMANn/CSI_Project/database/csi_data.db'
OUTPUT_CSV = 'd:/SUPERMANn/CSI_Project/CSI_cleaned_v2.csv'

print("="*80)
print("CSI DATA CLEANING SCRIPT")
print("="*80)

# Read from database
print("\n1. Reading data from database...")
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM csi_items", conn)
conn.close()

print(f"   Total rows in database: {len(df)}")

# Analyze data quality
print("\n2. Analyzing data quality...")
print(f"   Rows with NULL daily_output: {df['daily_output'].isna().sum()}")
print(f"   Rows with NULL man_hours: {df['man_hours'].isna().sum()}")
print(f"   Rows with NULL description: {df['description'].isna().sum()}")

# Identify header rows (rows without productivity data)
print("\n3. Identifying header rows...")
header_rows = df[df['daily_output'].isna() & df['man_hours'].isna()].copy()
print(f"   Found {len(header_rows)} header/division rows")

# Keep only data rows (rows with productivity data)
print("\n4. Filtering data rows...")
data_rows = df[df['daily_output'].notna() | df['man_hours'].notna()].copy()
print(f"   Kept {len(data_rows)} data rows with productivity information")

# Clean codes - remove extra spaces
print("\n5. Cleaning codes...")
for col in ['main_div_code', 'sub_div1_code', 'sub_div2_code', 'item_code']:
    if col in data_rows.columns:
        data_rows[col] = data_rows[col].astype(str).str.strip()

# Replace 'None' and 'nan' strings with actual None
print("\n6. Handling NA values...")
for col in data_rows.columns:
    data_rows[col] = data_rows[col].replace(['None', 'nan', 'NaN', ''], None)

# Validate crew structure
print("\n7. Validating crew structure...")
has_crew = data_rows['crew_structure'].notna().sum()
print(f"   Rows with crew structure: {has_crew}")
print(f"   Rows without crew structure: {len(data_rows) - has_crew}")

# Sample some cleaned data
print("\n8. Sample of cleaned data:")
print("-"*80)
sample = data_rows[data_rows['crew_structure'].notna()].head(3)
for idx, row in sample.iterrows():
    print(f"\nCode: {row['full_code']}")
    print(f"Description: {row['description'][:60]}...")
    print(f"Unit: {row['unit']}")
    print(f"Daily Output: {row['daily_output']}")
    print(f"Man Hours: {row['man_hours']}")
    print(f"Crew: {row['crew_structure'][:70]}...")
    print("-"*80)

# Save cleaned data
print("\n9. Saving cleaned data to CSV...")
data_rows.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
print(f"   [OK] Saved to: {OUTPUT_CSV}")

# Statistics
print("\n" + "="*80)
print("CLEANING SUMMARY")
print("="*80)
print(f"Original rows:        {len(df)}")
print(f"Header rows removed:  {len(header_rows)}")
print(f"Clean data rows:      {len(data_rows)}")
print(f"Reduction:            {len(header_rows)} rows ({(len(header_rows)/len(df)*100):.1f}%)")
print(f"\nRows with complete crew data: {has_crew} ({(has_crew/len(data_rows)*100):.1f}%)")
print(f"Output file: {OUTPUT_CSV}")
print("="*80)

# Create a summary of divisions
print("\n10. Division breakdown:")
div_summary = data_rows.groupby('main_div_code').agg({
    'full_code': 'count',
    'crew_structure': lambda x: x.notna().sum()
}).rename(columns={'full_code': 'total_items', 'crew_structure': 'items_with_crew'})
print(div_summary)

print("\n[SUCCESS] Data cleaning completed successfully!")
print(f"[FILE] Clean CSV ready at: {OUTPUT_CSV}")
