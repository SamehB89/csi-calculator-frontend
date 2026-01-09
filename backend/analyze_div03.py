import sqlite3

conn = sqlite3.connect('csi_data.db')
c = conn.cursor()

print("=" * 100)
print("DIVISION 03 - CONCRETE STRUCTURE ANALYSIS")
print("=" * 100)

# Get all sub-divisions in Division 03
print("\n--- Sub-Divisions in Division 03 ---")
c.execute("SELECT DISTINCT sub_div1_code, sub_div1_name FROM csi_items WHERE main_div_code = '03' ORDER BY sub_div1_code")
for r in c.fetchall():
    print(f"{r[0]} | {r[1]}")

# Formwork items (031)
print("\n--- FORMWORK ITEMS (031) ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE full_code LIKE '031%' LIMIT 15")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Reinforcement items (032)
print("\n--- REINFORCEMENT ITEMS (032) ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE full_code LIKE '032%' LIMIT 15")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Cast-in-place items (033) - Footings
print("\n--- FOOTINGS/FOUNDATIONS ITEMS ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE description LIKE '%footing%' OR description LIKE '%foundation%' LIMIT 15")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Columns
print("\n--- COLUMN ITEMS ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE description LIKE '%column%' LIMIT 15")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Beams
print("\n--- BEAM ITEMS ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE description LIKE '%beam%' LIMIT 15")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Slabs
print("\n--- SLAB ITEMS ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE description LIKE '%slab%' LIMIT 15")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

conn.close()
