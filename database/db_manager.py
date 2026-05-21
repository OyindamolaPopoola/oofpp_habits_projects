import sqlite3
import os

DB_NAME = "habit_tracker.db"

def get_connection():
    """Establishes and returns a connection to the SQLite database with foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    # Force SQLite to honor Foreign Key relationships
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database():
    """Creates the structural tables for habits and tracking records if they do not exist."""
    connection = get_connection()
    cursor = connection.cursor()
    
    # 1. Create Habits Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        periodicity TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    
    # 2. Create Records Table (Tracking Check-ins)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        check_in_time TEXT NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
    );
    """)
    
    connection.commit()
    connection.close()