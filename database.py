import sqlite3
import os

DB_PATH = 'instance/patients.db'

def get_db_connection():
    """Create connection to SQLite database"""
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create patients table if not exists"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()
    conn.close()

def get_all_patients():
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients ORDER BY id DESC').fetchall()
    conn.close()
    return [dict(p) for p in patients]

def update_patient(pid, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_db_connection()
    conn.execute('''
        UPDATE patients
        SET full_name=?, date_of_birth=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
        WHERE id=?
    ''', (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, pid))
    conn.commit()
    conn.close()

def delete_patient(pid):
    conn = get_db_connection()
    conn.execute('DELETE FROM patients WHERE id=?', (pid,))
    conn.commit()
    conn.close()

def get_patient_by_id(pid):
    conn = get_db_connection()
    patient = conn.execute('SELECT * FROM patients WHERE id=?', (pid,)).fetchone()
    conn.close()
    return dict(patient) if patient else None
