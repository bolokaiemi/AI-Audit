import sqlite3
from datetime import datetime

DB_NAME = "audit.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        language_score INTEGER,
        instruction_score INTEGER,
        boundary_score INTEGER,
        overall_score INTEGER,
        status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_audit(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO audits (
        model_name,
        language_score,
        instruction_score,
        boundary_score,
        overall_score,
        status,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["model_name"],
        data["language_score"],
        data["instruction_score"],
        data["boundary_score"],
        data["overall_score"],
        data["status"],
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()