import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

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
        role TEXT,
        api_key TEXT,
        email TEXT UNIQUE
    )
    """)

    # Ensure api_key column exists (migration helper)
    try:
        cur.execute("ALTER TABLE users ADD COLUMN api_key TEXT")
    except sqlite3.OperationalError:
        pass

    # Ensure email column exists (migration helper)
    try:
        cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass

    # Backfill missing API keys
    cur.execute("SELECT id FROM users WHERE api_key IS NULL")
    null_users = cur.fetchall()
    for u in null_users:
        new_key = "audit_" + secrets.token_hex(16)
        cur.execute("UPDATE users SET api_key = ? WHERE id = ?", (new_key, u[0]))

    # TRAINING REQUESTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS training_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        model_name TEXT,
        issue_description TEXT,
        contact_email TEXT,
        status TEXT DEFAULT 'PENDING',
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


def create_user(username, password, role="USER", email=None):
    conn = get_connection()
    cur = conn.cursor()
    hashed = generate_password_hash(password)
    api_key = "audit_" + secrets.token_hex(16)
    try:
        cur.execute("INSERT INTO users (username, password, role, api_key, email) VALUES (?, ?, ?, ?, ?)", (username, hashed, role, api_key, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
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


def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, role, api_key, email FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"username": row[0], "role": row[1], "api_key": row[2], "email": row[3]}
    return None


def update_user_password_by_email(email, new_password):
    conn = get_connection()
    cur = conn.cursor()
    hashed = generate_password_hash(new_password)
    cur.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
    conn.commit()
    conn.close()


def update_user_password(username, new_password):
    conn = get_connection()
    cur = conn.cursor()
    hashed = generate_password_hash(new_password)
    cur.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
    conn.commit()
    conn.close()


def get_user_by_api_key(api_key):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users WHERE api_key = ?", (api_key,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"username": row[0], "role": row[1]}
    return None


def get_api_key_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT api_key FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    return None


def reset_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM audits")
    cur.execute("DELETE FROM complaints")
    cur.execute("DELETE FROM training_requests")
    conn.commit()
    conn.close()


def create_training_request(username, model_name, issue_description, contact_email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO training_requests (username, model_name, issue_description, contact_email, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (username, model_name, issue_description, contact_email, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_training_requests():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, model_name, issue_description, contact_email, status, created_at FROM training_requests ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_training_requests(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, model_name, issue_description, contact_email, status, created_at FROM training_requests WHERE username = ? ORDER BY id DESC", (username,))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_training_request_status(request_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE training_requests SET status = ? WHERE id = ?", (status, request_id))
    conn.commit()
    conn.close()


def get_training_request_by_id(request_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, model_name, issue_description, contact_email, status, created_at FROM training_requests WHERE id = ?", (request_id,))
    row = cur.fetchone()
    conn.close()
    return row
