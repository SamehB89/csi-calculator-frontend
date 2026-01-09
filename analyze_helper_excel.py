import pandas as pd
import sys

try:
    # Read the Excel file
    excel_file = r'd:\SUPERMANn\CSI_Project\مساعد المساعد الذكي.xlsx'
    
    # Get sheet names
    xl = pd.ExcelFile(excel_file)
    print("=" * 80)
    print(f"📊 EXCEL FILE ANALYSIS: مساعد المساعد الذكي.xlsx")
    print("=" * 80)
    print(f"\n📋 Sheets found: {len(xl.sheet_names)}")
    for i, sheet in enumerate(xl.sheet_names, 1):
        print(f"   {i}. {sheet}")
    
    # Analyze each sheet
    for sheet_name in xl.sheet_names:
        print(f"\n{'=' * 80}")
        print(f"📄 SHEET: {sheet_name}")
        print("=" * 80)
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        print(f"\n📊 Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"\n📝 Columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        
        print(f"\n🔍 Sample Data (first 5 rows):")
        print(df.head(5).to_string(index=False))
        
        print(f"\n📈 Data Summary:")
        print(f"   - Non-null values per column:")
        for col in df.columns:
            non_null = df[col].notna().sum()
            print(f"     • {col}: {non_null}/{len(df)} ({non_null/len(df)*100:.1f}%)")
    
    print(f"\n{'=' * 80}")
    print("✅ Analysis Complete")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
