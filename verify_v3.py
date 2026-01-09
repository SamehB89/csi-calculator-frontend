import sqlite3
import os

DB_PATH = os.path.join('database', 'csi_data.db')

def verify():
    print(f"Checking {DB_PATH}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        assemblies = conn.execute("SELECT * FROM assemblies").fetchall()
        print(f"Assemblies found: {len(assemblies)}")
        for a in assemblies:
            print(f"- {a[1]} ({a[2]})")
            
        components = conn.execute("SELECT * FROM assembly_components").fetchall()
        print(f"Components found: {len(components)}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    verify()
