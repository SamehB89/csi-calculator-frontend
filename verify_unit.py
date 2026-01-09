import sqlite3

conn = sqlite3.connect('database/csi_data.db')
c = conn.cursor()

c.execute('''SELECT full_code, description, unit, daily_output 
             FROM csi_items 
             WHERE full_code = '031 158-5150' ''')

row = c.fetchone()
if row:
    print(f"Code: {row[0]}")
    print(f"Description: {row[1]}")
    print(f"Unit: {row[2]}")
    print(f"Daily Output: {row[3]}")
else:
    print("Item not found!")

conn.close()
