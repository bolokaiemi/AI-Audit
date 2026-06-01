import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "audit.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # AUDITS
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

    # COMPLAINTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        issue TEXT,
        severity TEXT,
        created_at TEXT,
        status TEXT DEFAULT 'OPEN'
    )
    """)

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
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


def save_complaint(model_name, issue, severity="MEDIUM"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO complaints (
        model_name, issue, severity, created_at
    )
    VALUES (?, ?, ?, ?)
    """, (
        model_name,
        issue,
        severity,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_audits():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM audits ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows


def get_complaints():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM complaints ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows


def get_audits_by_model(model_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM audits WHERE model_name = ? ORDER BY id DESC", (model_name,))
    rows = cur.fetchall()

    conn.close()
    return rows


def create_user(username, password, role="USER"):
    conn = get_connection()
    cur = conn.cursor()
    hashed = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()


def verify_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, role, password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and check_password_hash(row[2], password):
        return {"username": row[0], "role": row[1]}
    return None


def update_user_password(username, new_password):
    conn = get_connection()
    cur = conn.cursor()
    hashed = generate_password_hash(new_password)
    cur.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
    conn.commit()
    conn.close()
