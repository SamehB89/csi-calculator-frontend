import sqlite3
import pandas as pd

db_path = 'database/csi_data.db'

print(f"Connecting to {db_path}...")
conn = sqlite3.connect(db_path)

# Query to find the specific item
print("\n--- Inspecting Item '034 802' ---")
query = "SELECT * FROM csi_items WHERE sub_div2_code LIKE '%034 802%' OR description LIKE '%LINTEL%'"
df = pd.read_sql_query(query, conn)

if not df.empty:
    print(df[['main_div_code', 'main_div_name', 'sub_div1_code', 'sub_div1_name', 'sub_div2_code', 'sub_div2_name', 'item_code', 'description']])
else:
    print("Item not found.")

# Query to see what Sub-Division 1 '4' contains
print("\n--- Inspecting Sub-Division 1 code '4' ---")
query2 = "SELECT DISTINCT main_div_code, main_div_name, sub_div1_code, sub_div1_name FROM csi_items WHERE sub_div1_code = '4'"
df2 = pd.read_sql_query(query2, conn)
print(df2)

conn.close()
