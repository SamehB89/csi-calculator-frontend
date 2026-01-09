# -*- coding: utf-8 -*-
"""
Script to migrate data from local SQLite database to Turso cloud database
"""
import sqlite3
import os
import sys

# Turso configuration
TURSO_DATABASE_URL = "libsql://csi-calculator-samehb89.aws-eu-west-1.turso.io"
TURSO_AUTH_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NjU0NTAzOTksImlkIjoiMDZiZjZjOGItYWRmOS00NTYyLTg0MmQtM2I4MzZiZGU3ZDQ0IiwicmlkIjoiYmQ3NmNiMDQtOTIxYi00OWRiLThkZmMtYTFmZTcyODQ4ZTM4In0.I6xwx2Wc_KfQGgCv8DRTaHQTXEjUqIbfo9tmpKwCnuOmtGv-5BjkiguS0GhFiaLavzP7rikXVN5piVLvKigiDw"

# Local database path
LOCAL_DB_PATH = os.path.join(os.path.dirname(__file__), 'backend', 'csi_data.db')

def migrate_to_turso():
    """Migrate all data from local SQLite to Turso"""
    
    print("=" * 80)
    print("CSI Calculator - Database Migration to Turso")
    print("=" * 80)
    print()
    
    # Step 1: Connect to local SQLite
    print("[1/7] Connecting to local SQLite database...")
    try:
        local_conn = sqlite3.connect(LOCAL_DB_PATH)
        local_conn.row_factory = sqlite3.Row
        local_cursor = local_conn.cursor()
        print(f"   [OK] Connected to: {LOCAL_DB_PATH}")
    except Exception as e:
        print(f"   [ERROR] Failed to connect to local database: {e}")
        return False
    
    # Step 2: Connect to Turso
    print("\n[2/7] Connecting to Turso cloud database...")
    try:
        import libsql_client
        turso_client = libsql_client.create_client_sync(
            url=TURSO_DATABASE_URL,
            auth_token=TURSO_AUTH_TOKEN
        )
        print(f"   [OK] Connected to: {TURSO_DATABASE_URL}")
    except ImportError:
        print("   [ERROR] libsql-client not installed!")
        print("   Run: pip install libsql-client")
        return False
    except Exception as e:
        print(f"   [ERROR] Failed to connect to Turso: {e}")
        return False
    
    # Step 3: Get table schema
    print("\n[3/7] Reading table schema...")
    try:
        local_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables_schema = local_cursor.fetchall()
        print(f"   [OK] Found {len(tables_schema)} table(s)")
    except Exception as e:
        print(f"   [ERROR] Failed to read schema: {e}")
        return False
    
    # Step 4: Create tables in Turso
    print("\n[4/7] Creating tables in Turso...")
    for schema_row in tables_schema:
        schema_sql = schema_row['sql']
        table_name = schema_sql.split('CREATE TABLE')[1].split('(')[0].strip().strip('"').strip("'")
        
        try:
            # Drop table if exists
            turso_client.execute(f"DROP TABLE IF EXISTS {table_name}")
            # Create table
            turso_client.execute(schema_sql)
            print(f"   [OK] Created table: {table_name}")
        except Exception as e:
            print(f"   [WARNING] For table {table_name}: {e}")
    
    # Step 5: Get all table names
    print("\n[5/7] Getting table list...")
    local_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row['name'] for row in local_cursor.fetchall()]
    print(f"   [OK] Tables to migrate: {', '.join(tables)}")
    
    # Step 6: Migrate data
    print("\n[6/7] Migrating data...")
    total_rows = 0
    
    for table_name in tables:
        print(f"\n   Migrating table: {table_name}")
        
        try:
            # Get all data from local table
            local_cursor.execute(f"SELECT * FROM {table_name}")
            rows = local_cursor.fetchall()
            
            if not rows:
                print(f"      Table is empty")
                continue
            
            # Get column names
            columns = [description[0] for description in local_cursor.description]
            
            # Insert data into Turso batch by batch
            batch_size = 100
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i+batch_size]
                
                for row in batch:
                    placeholders = ','.join(['?' for _ in columns])
                    columns_str = ','.join(columns)
                    insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                    
                    try:
                        turso_client.execute(insert_sql, list(row))
                    except Exception as e:
                        print(f"      [WARNING] Failed to insert row: {e}")
                
                print(f"      Progress: {min(i+batch_size, len(rows))}/{len(rows)} rows")
            
            total_rows += len(rows)
            print(f"      [OK] Completed: {len(rows)} rows migrated")
            
        except Exception as e:
            print(f"      [ERROR] Failed to migrate {table_name}: {e}")
    
    # Step 7: Verify migration
    print(f"\n[7/7] Verifying migration...")
    print(f"   Total rows migrated: {total_rows}")
    
    for table_name in tables:
        try:
            # Count rows in Turso
            result = turso_client.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            turso_count = result.rows[0]['count'] if result.rows else 0
            
            # Count rows in local
            local_cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            local_count = local_cursor.fetchone()['count']
            
            status = "[OK]" if turso_count == local_count else "[ERROR]"
            print(f"   {status} {table_name}: Local={local_count}, Turso={turso_count}")
            
        except Exception as e:
            print(f"   [WARNING] Could not verify {table_name}: {e}")
    
    # Cleanup
    local_conn.close()
    
    print("\n" + "=" * 80)
    print("Migration completed!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("   1. Set environment variables in Railway:")
    print(f"      TURSO_DATABASE_URL={TURSO_DATABASE_URL}")
    print("      TURSO_AUTH_TOKEN=[your-token]")
    print("      GEMINI_API_KEY=[your-key]")
    print()
    print("   2. Deploy to Railway")
    print("   3. Test the application")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = migrate_to_turso()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
