import pandas as pd

# Read with proper headers
df = pd.read_excel('CSI.xlsm', engine='openpyxl', header=1)

print("="*100)
print("COMPLETE DATA STRUCTURE ANALYSIS")
print("="*100)

# Display all columns with their index
print("\nALL COLUMNS (with index):")
print("-"*100)
for i, col in enumerate(df.columns):
    print(f"{i:3d}. {col}")

# Get column by index to understand structure
print("\n" + "="*100)
print("ANALYZING DATA STRUCTURE")
print("="*100)

# Find rows with actual data (skip header rows)
print("\nSearching for data rows...")
for idx in range(5, 100):
    row = df.iloc[idx]
    # Check if row has item description
    item_desc = row.iloc[7] if len(row) > 7 else None  # Column 7 based on previous output
    
    if pd.notna(item_desc) and str(item_desc).strip() and len(str(item_desc)) > 5:
        print(f"\n{'='*100}")
        print(f"SAMPLE ITEM RECORD (Row {idx})")
        print(f"{'='*100}")
        
        for i, col in enumerate(df.columns):
            val = row.iloc[i]
            if pd.notna(val) and str(val).strip():
                print(f"{col:30s}: {val}")
        
        print(f"\n{'='*100}")
        print("CREW DETAILS FROM THIS RECORD")
        print(f"{'='*100}")
        
        for i in range(1, 14):
            crew_num_col = f'Crew Number{i}'
            crew_desc_col = f'Crew Desc.{i}'
            
            if crew_num_col in df.columns and crew_desc_col in df.columns:
                crew_num = row[crew_num_col]
                crew_desc = row[crew_desc_col]
                
                if pd.notna(crew_num) or pd.notna(crew_desc):
                    print(f"  Crew {i:2d}: Num={crew_num}, Desc={crew_desc}")
        
        break

# Analyze unique values in key columns
print(f"\n{'='*100}")
print("UNIQUE VALUES ANALYSIS")
print(f"{'='*100}")

# Try to identify the hierarchical columns
col_list = df.columns.tolist()
print(f"\nTotal rows: {len(df)}")

# Check each column for unique values
for col in col_list[:15]:  # First 15 columns likely contain divisions
    unique_count = df[col].nunique()
    non_null_count = df[col].notna().sum()
    print(f"{col:30s}: {unique_count:5d} unique values, {non_null_count:5d} non-null")

# Save to CSV for easier API usage
print(f"\n{'='*100}")
print("Saving to CSI_latest.csv...")
df.to_csv('CSI_latest.csv', index=False, encoding='utf-8-sig')
print("Done!")
