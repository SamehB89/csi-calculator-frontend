# -*- coding: utf-8 -*-
"""
Script to migrate data from local SQLite database to Neon PostgreSQL
"""
import sqlite3
import os
import sys

# Neon PostgreSQL configuration
POSTGRES_URL = "postgresql://neondb_owner:npg_NEGDI4es3ZVO@ep-young-butterfly-agyqank4-pooler.c-2.eu-central-1.aws.neon.tech/CSI_Calculator?sslmode=require"

# Local database path
LOCAL_DB_PATH = os.path.join(os.path.dirname(__file__), 'backend', 'csi_data.db')

def migrate_to_postgres():
    """Migrate all data from local SQLite to Neon PostgreSQL"""
    
    print("=" * 80)
    print("CSI Calculator - Database Migration to PostgreSQL")
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
    
    # Step 2: Connect to PostgreSQL
    print("\n[2/7] Connecting to Neon PostgreSQL...")
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        pg_conn = psycopg2.connect(POSTGRES_URL)
        pg_cursor = pg_conn.cursor(cursor_factory=RealDictCursor)
        print(f"   [OK] Connected to PostgreSQL")
    except ImportError:
        print("   [ERROR] psycopg2 not installed!")
        print("   Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"   [ERROR] Failed to connect to PostgreSQL: {e}")
        return False
    
    # Step 3: Get table schema
    print("\n[3/7] Reading SQLite schema...")
    try:
        local_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables_schema = local_cursor.fetchall()
        print(f"   [OK] Found {len(tables_schema)} table(s)")
    except Exception as e:
        print(f"   [ERROR] Failed to read schema: {e}")
        return False
    
    # Step 4: Convert and create tables in PostgreSQL
    print("\n[4/7] Creating tables in PostgreSQL...")
    for schema_row in tables_schema:
        table_name = schema_row['name']
        sqlite_sql = schema_row['sql']
        
        try:
            # Convert SQLite schema to PostgreSQL
            pg_sql = convert_schema_to_postgres(sqlite_sql)
            
            # Drop table if exists
            pg_cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
            
            # Create table
            pg_cursor.execute(pg_sql)
            pg_conn.commit()
            
            print(f"   [OK] Created table: {table_name}")
        except Exception as e:
            print(f"   [WARNING] For table {table_name}: {e}")
            pg_conn.rollback()
    
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
            
            # Insert data into PostgreSQL using batch inserts
            batch_size = 500
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i+batch_size]
                
                # Build batch insert query
                placeholders = ','.join(['%s' for _ in columns])
                columns_str = ','.join([f'"{col}"' for col in columns])
                insert_sql = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})'
                
                # Prepare batch data
                batch_data = [tuple(row) for row in batch]
                
                try:
                    # Execute batch insert
                    from psycopg2.extras import execute_batch
                    execute_batch(pg_cursor, insert_sql, batch_data, page_size=100)
                    pg_conn.commit()
                    
                    print(f"      Progress: {min(i+batch_size, len(rows))}/{len(rows)} rows")
                except Exception as e:
                    print(f"      [WARNING] Batch insert failed: {e}")
                    pg_conn.rollback()
                    
                    # Try row-by-row insert as fallback
                    for row in batch:
                        try:
                            pg_cursor.execute(insert_sql, tuple(row))
                            pg_conn.commit()
                        except Exception as row_error:
                            print(f"      [WARNING] Failed to insert row: {row_error}")
                            pg_conn.rollback()
            
            total_rows += len(rows)
            print(f"      [OK] Completed: {len(rows)} rows migrated")
            
        except Exception as e:
            print(f"      [ERROR] Failed to migrate {table_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Step 7: Verify migration
    print(f"\n[7/7] Verifying migration...")
    print(f"   Total rows migrated: {total_rows}")
    
    for table_name in tables:
        try:
            # Count rows in PostgreSQL
            pg_cursor.execute(f'SELECT COUNT(*) as count FROM "{table_name}"')
            pg_count = pg_cursor.fetchone()['count']
            
            # Count rows in local
            local_cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            local_count = local_cursor.fetchone()['count']
            
            status = "[OK]" if pg_count == local_count else "[ERROR]"
            print(f"   {status} {table_name}: Local={local_count}, PostgreSQL={pg_count}")
            
        except Exception as e:
            print(f"   [WARNING] Could not verify {table_name}: {e}")
    
    # Cleanup
    local_conn.close()
    pg_conn.close()
    
    print("\n" + "=" * 80)
    print("Migration completed!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("   1. Set environment variables in Railway:")
    print(f"      DATABASE_URL={POSTGRES_URL}")
    print("      GEMINI_API_KEY=[your-key]")
    print()
    print("   2. Deploy to Railway")
    print("   3. Test the application")
    print()
    
    return True


def convert_schema_to_postgres(sqlite_sql):
    """
    Convert SQLite CREATE TABLE statement to PostgreSQL compatible format
    """
    # Replace SQLite types with PostgreSQL types
    pg_sql = sqlite_sql
    
    # Type conversions
    pg_sql = pg_sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    pg_sql = pg_sql.replace('INTEGER PRIMARY KEY', 'SERIAL PRIMARY KEY')
    pg_sql = pg_sql.replace('AUTOINCREMENT', '')
    
    # SQLite uses TEXT for all strings, PostgreSQL is more specific
    # But TEXT works fine in PostgreSQL too, so we keep it
    
    # Handle quoted identifiers - PostgreSQL prefers double quotes
    # SQLite accepts both, let's normalize
    import re
    
    # Find table name and ensure it's properly quoted
    match = re.search(r'CREATE TABLE\s+["`]?(\w+)["`]?\s*\(', pg_sql, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        pg_sql = re.sub(
            r'CREATE TABLE\s+["`]?\w+["`]?\s*\(',
            f'CREATE TABLE "{table_name}" (',
            pg_sql,
            flags=re.IGNORECASE
        )
    
    return pg_sql


if __name__ == "__main__":
    try:
        success = migrate_to_postgres()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
