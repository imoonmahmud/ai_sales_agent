import sqlite3
from datetime import date

conn = sqlite3.connect('leads.db')
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            industry TEXT,
            employee_count INTEGER,
            website TEXT,
            source TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)

    conn.commit()

def add_lead(company_name, industry, employee_count, website, source, notes):
    cursor.execute(
        """
        INSERT INTO leads (
            company_name,
            industry,
            employee_count,
            website,
            source,
            notes,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            company_name,
            industry,
            employee_count,
            website,
            source,
            notes,
            date.today().isoformat()
        )
    )

    conn.commit()


def get_all_leads():
    cursor.execute("SELECT * FROM leads")
    return cursor.fetchall()
