# -*- coding: utf-8 -*-
# Test PostgreSQL connection with db_config
import os
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_NEGDI4es3ZVO@ep-young-butterfly-agyqank4-pooler.c-2.eu-central-1.aws.neon.tech/CSI_Calculator?sslmode=require'

from backend.db_config import get_db_connection

print("Testing PostgreSQL connection...")
conn = get_db_connection()

# Test query
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM csi_items")
result = cursor.fetchone()

print(f"[OK] Connection successful!")
print(f"[OK] CSI Items count: {result[0] if result else 'N/A'}")

# Test a sample query
cursor.execute("SELECT * FROM csi_items LIMIT 5")
rows = cursor.fetchall()
print(f"[OK] Sample data retrieved: {len(rows)} rows")

for row in rows:
    code = row['Code'] if 'Code' in row else row.get('code', 'N/A')
    desc = row['Description'] if 'Description' in row else row.get('description', 'N/A')
    print(f"  - {code}: {desc[:50]}")

conn.close()
print("\n[OK] All tests passed!")
