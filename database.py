import json
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
            contact_name TEXT,
            contact_role TEXT,
            contact_email TEXT,
            score INTEGER,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()

def add_lead(
        company_name, 
        industry,
        employee_count, 
        website, 
        source,
        notes,
        contact_name,
        contact_role,
        contact_email,
        score,
        status):
    cursor.execute(
        """
        INSERT INTO leads (
            company_name,
            industry,
            employee_count,
            website,
            source,
            notes,
            contact_name,
            contact_role,
            contact_email,
            score,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            company_name,
            industry,
            employee_count,
            website,
            source,
            notes,
            contact_name,
            contact_role,
            contact_email,
            score,
            status,
            date.today().isoformat()
        )
    )
    conn.commit()


def get_all_leads():
    cursor.execute("SELECT * FROM leads")
    return cursor.fetchall()


def load_sample_leads():
    with open('data/sample_dataset.json', 'r') as file:
        leads = json.load(file)

    return leads

def flatten_lead(record):
    company = record.get('company')

    return {
        'company_name': company.get('name'),
        'industry': company.get('industry'),
        'employee_count': company.get('employeeCount'),
        'website': f"https://{company.get('domain')}",
        'source': 'sample_data',
        'notes': f"Sub-industry: {company.get('subIndustry')}; Revenue: ${company.get('revenue'):,}",
        'contact_name': record.get('fullName'),
        'contact_role': record.get('jobTitle'),
        'contact_email': record.get('email')
    }

if __name__ == '__main__':
    leads = load_sample_leads()
    for record in leads:
        flat = flatten_lead(record)
        print(flat)
