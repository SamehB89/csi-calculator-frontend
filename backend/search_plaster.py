import sqlite3

conn = sqlite3.connect('csi_data.db')
c = conn.cursor()

print("=" * 80)
print("SEARCHING FOR ALL PLASTER-RELATED ITEMS IN DATABASE")
print("=" * 80)

# Search for Portland cement items
print("\n--- Section 092 4XX (Portland Cement Plastering) ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE full_code LIKE '092 4%' LIMIT 15")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Search for any items with 'cement' and 'plaster'
print("\n--- Items containing 'cement' and 'plaster' ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE description LIKE '%cement%' AND description LIKE '%plaster%' LIMIT 10")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Search for stucco (external plaster)
print("\n--- Stucco items ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE description LIKE '%stucco%' LIMIT 10")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Search for items on masonry
print("\n--- Items on masonry ---")
c.execute("SELECT full_code, description, unit, daily_output FROM csi_items WHERE description LIKE '%masonry%' LIMIT 10")
for r in c.fetchall():
    print(f"{r[0]} | {r[1][:60]} | {r[2]} | {r[3]}")

# Show all Sub-Division 1 names in Division 09
print("\n--- All Sub-Divisions in Division 09 ---")
c.execute("SELECT DISTINCT sub_div1_code, sub_div1_name FROM csi_items WHERE main_div_code = '09' ORDER BY sub_div1_code")
for r in c.fetchall():
    print(f"{r[0]} | {r[1]}")

conn.close()
