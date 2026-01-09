import pandas as pd

# Read with proper headers (row 1 as header)
df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)

print(f"{'='*80}")
print(f"DATA STRUCTURE ANALYSIS")
print(f"{'='*80}\n")

# Clean up column names
df.columns = df.columns.str.strip()

# Show a few complete records
print("Sample Item with all details:")
print("-" * 80)

# Find a row with crew data
for idx in range(10, 50):
    row = df.iloc[idx]
    if pd.notna(row.get('ITEM DESCRIPTION', None)):
        print(f"\nMain Division: {row.get('Main_Division', 'N/A')}")
        print(f"Sub-Division 1: {row.get('Sub_Division1', 'N/A')}")
        print(f"Sub-Division 2: {row.get('Sub_Division2', 'N/A')}")
        print(f"Item Description: {row.get('ITEM DESCRIPTION', 'N/A')}")
        print(f"Daily Output: {row.get('DAILY OUTPUT', 'N/A')}")
        print(f"Man Hours: {row.get('MAN HOURS', 'N/A')}")
        print(f"Equip Hours: {row.get('EQUIP. HOURS', 'N/A')}")
        print(f"Crew Structure Combined: {row.get('CREW STRUCTURE COMBINED', 'N/A')}")
        
        print("\nCrew Details:")
        for i in range(1, 13):
            crew_num = row.get(f'Crew Number{i}', None)
            crew_desc = row.get(f'Crew Desc.{i}', None)
            if pd.notna(crew_num) or pd.notna(crew_desc):
                print(f"  Crew {i}: Number={crew_num}, Desc={crew_desc}")
        
        break

# Get unique counts
print(f"\n{'='*80}")
print(f"HIERARCHICAL STRUCTURE COUNTS")
print(f"{'='*80}")
print(f"Unique Main Divisions: {df['Main_Division'].nunique()}")
print(f"Unique Sub-Division 1: {df['Sub_Division1'].nunique()}")
print(f"Unique Sub-Division 2: {df['Sub_Division2'].nunique()}")
print(f"Unique Item Descriptions: {df['ITEM DESCRIPTION'].nunique()}")

print(f"\n{'='*80}")
print(f"MAIN DIVISIONS")
print(f"{'='*80}")
main_divs = df['Main_Division'].dropna().unique()
for md in sorted([str(x) for x in main_divs if str(x) != 'nan'])[:20]:
    print(f"  {md}")

# Save cleaned version to CSV for API use
print(f"\n{'='*80}")
print("Saving cleaned data to CSI_latest.csv...")
df.to_csv('CSI_latest.csv', index=False, encoding='utf-8-sig')
print("Done!")
