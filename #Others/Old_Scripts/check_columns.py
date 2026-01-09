import pandas as pd
import json

# Read with proper headers (row 1 as header)
df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)

print(f"{'='*80}")
print(f"ACTUAL COLUMN NAMES")
print(f"{'='*80}\n")
for i, col in enumerate(df.columns, 1):
    print(f"{i:3d}. '{col}'")

print(f"\n{'='*80}")
print(f"FIRST 3 ROWS")
print(f"{'='*80}\n")
print(df.head(3).to_string())

# Try to identify the correct column names
print(f"\n{'='*80}")
print(f"SEARCHING FOR KEY COLUMNS")
print(f"{'='*80}\n")

# Look for main division column
for col in df.columns:
    if 'main' in str(col).lower() or 'division' in str(col).lower():
        print(f"Division-related column: '{col}'")
    if 'item' in str(col).lower() and 'desc' in str(col).lower():
        print(f"Item Description column: '{col}'")
    if 'output' in str(col).lower():
        print(f"Output column: '{col}'")
    if 'crew' in str(col).lower():
        print(f"Crew column: '{col}'")
