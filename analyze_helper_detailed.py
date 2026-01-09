import pandas as pd

# Read the Excel file
excel_file = r'd:\SUPERMANn\CSI_Project\مساعد المساعد الذكي.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet1')

# Clean column names
df.columns = ['محتوى', 'col2', 'col3', 'col4']

print("=" * 100)
print("📊 DETAILED CONTENT ANALYSIS")
print("=" * 100)

# Show rows 10-30 to see the actual data structure
print("\n🔍 Sample rows (10-30):")
print(df.iloc[10:30].to_string(index=True))

print("\n" + "=" * 100)
print("📋 DATA CATEGORIZATION")
print("=" * 100)

# Try to identify patterns
non_null_rows = df[df['محتوى'].notna()]
print(f"\n✅ Rows with content: {len(non_null_rows)}")

# Show a few more sample rows
print("\n🔍 More samples (rows 40-55):")
print(df.iloc[40:55].to_string(index=True))

print("\n🔍 Last few rows (100-110):")
print(df.iloc[100:].to_string(index=True))
