import sqlite3

db_path = r'd:\SUPERMANn\CSI_Project\backend\csi_data.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Searching for item_code='1000' AND daily_output=14...")
    cursor.execute("SELECT full_code, description, daily_output, unit FROM csi_items WHERE item_code = '1000' AND daily_output = 14")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} rows:")
    for row in rows:
        print(row)
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
