"""
Database configuration module for CSI Calculator
Uses local SQLite database for simplicity and reliability
"""
import os
import sqlite3

# Local SQLite path
DB_PATH = os.path.join(os.path.dirname(__file__), 'csi_data.db')

def get_db_connection():
    """
    Get SQLite database connection.
    Simple and reliable - no cloud dependencies.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Print configuration on module load
print(f"[INFO] Using SQLite database: {DB_PATH}")
