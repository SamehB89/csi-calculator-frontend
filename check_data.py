import sqlite3

conn = sqlite3.connect('database/csi_data.db')
c = conn.cursor()

# Find items with code 706
c.execute('''SELECT full_code, main_div_name, sub_div1_name, sub_div2_name, description 
             FROM csi_items 
             WHERE full_code LIKE '%020 706%' OR item_code LIKE '%706%'
             LIMIT 10''')

print("Items with code 706:")
print("-" * 150)
print(f"{'Code':<20} | {'Main Division':<30} | {'Sub-Div 1':<30} | {'Sub-Div 2':<30} | {'Description':<40}")
print("-" * 150)

for row in c.fetchall():
    code, main, sub1, sub2, desc = row
    print(f"{code or 'None':<20} | {main or 'None':<30} | {sub1 or 'None':<30} | {sub2 or 'None':<30} | {(desc or 'None')[:40]:<40}")

conn.close()
