import pandas as pd

# Read the Excel file
print("Reading CSI.xlsm...")
df = pd.read_excel('CSI.xlsm', engine='openpyxl')

print(f"\n{'='*80}")
print(f"BASIC INFO")
print(f"{'='*80}")
print(f"Shape: {df.shape}")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print(f"\n{'='*80}")
print(f"ALL COLUMNS")
print(f"{'='*80}")
for i, col in enumerate(df.columns, 1):
    print(f"{i:3d}. {col}")

print(f"\n{'='*80}")
print(f"FIRST 5 ROWS (Raw)")
print(f"{'='*80}")
print(df.head(5))

# Try reading with header row 1
print(f"\n{'='*80}")
print(f"READING WITH HEADER=1")
print(f"{'='*80}")
df2 = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)
print(f"Shape: {df2.shape}")
print("\nColumns:")
for i, col in enumerate(df2.columns, 1):
    print(f"{i:3d}. {col}")

print(f"\n{'='*80}")
print(f"SAMPLE DATA (with header=1)")
print(f"{'='*80}")
print(df2.head(3))

# Check for crew columns
crew_cols = [col for col in df2.columns if 'Crew' in str(col)]
print(f"\n{'='*80}")
print(f"CREW COLUMNS FOUND")
print(f"{'='*80}")
for col in crew_cols:
    print(f"  - {col}")
