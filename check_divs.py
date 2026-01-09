import sqlite3

conn = sqlite3.connect('database/csi_data.db')
c = conn.cursor()

# Get divisions
c.execute('SELECT main_div_code, main_div_name FROM csi_items GROUP BY main_div_code ORDER BY main_div_code')
divs = c.fetchall()

print(f'Total divisions: {len(divs)}')
for d in divs:
    print(f'{d[0]} - {d[1]}')

conn.close()
