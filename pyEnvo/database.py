# Envo Userbot - SQLite Database
# Created by @envologia

import sqlite3

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect("envo.db")
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Initializes the database and creates the tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create AFK table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS afk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            is_afk BOOLEAN NOT NULL,
            reason TEXT,
            start_time REAL
        )
    """)

    # Create PM Security table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approved_users (
            user_id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()

# Initialize the database when the module is loaded
initialize_database()
