import json
import sqlite3
from datetime import date, datetime

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

def rows_to_dicts(cursor, rows):
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def init_outreach_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outreach (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            email_subject TEXT,
            email_body TEXT,
            status TEXT DEFAULT 'pending_approval',
            created_at TEXT,
            reviewed_at TEXT,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
    """)
    conn.commit()

def add_sent_at_column():
    cursor.execute('ALTER TABLE outreach ADD COLUMN sent_at TEXT')
    conn.commit()

def save_outreach_draft(lead_id, subject, body):
    cursor.execute(
        """
        INSERT INTO outreach (
            lead_id,
            email_subject,
            email_body,
            created_at,
            reviewed_at
        )
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            lead_id,
            subject,
            body,
            date.today().isoformat(),
            None
        )
    )
    conn.commit()

def get_outreach_draft():
    cursor.execute("SELECT * FROM outreach")
    return cursor.fetchall()

def get_pending_outreach():
    cursor.execute("""
        SELECT
            outreach.id,
            outreach.lead_id,
            outreach.email_subject,
            outreach.email_body,
            outreach.status,
            outreach.created_at,
            leads.company_name,
            leads.contact_name,
            leads.contact_role,
            leads.contact_email
        FROM outreach
        JOIN leads
            ON outreach.lead_id = leads.id
        WHERE outreach.status = 'pending_approval'
    """)
    rows = cursor.fetchall()
    return rows_to_dicts(cursor, rows)


def update_outreach_status(outreach_id, new_status):
    cursor.execute(
        """
        UPDATE outreach
        SET status = ?, reviewed_at = ?
        WHERE id = ?
    """, (new_status, date.today().isoformat(), outreach_id))
    conn.commit()

def review_pending_outreach():
    pending = get_pending_outreach()

    if not pending:
        print("No pending outreach to review.")
        return

    for outreach in pending:
        print("\n" + "=" * 50)
        print(f"Company: {outreach['company_name']}")
        print(f"Contact: {outreach['contact_name']} ({outreach['contact_role']})")
        print(f"Email: {outreach['contact_email']}")
        print(f"Subject: {outreach['email_subject']}")
        print(f"Body:\n{outreach['email_body']}")
        print("=" * 50)

        decision = input("Approve, reject, or skip? (a/r/s): ").strip().lower()

        if decision == "a":
            update_outreach_status(outreach['id'], "approved")
            print("Outreach approved.")

        elif decision == "r":
            update_outreach_status(outreach['id'], "rejected")
            print("Outreach rejected.")

        elif decision == "s":
            print("Skipped.")

        else:
            print("Invalid choice. Skipping.")

def get_approved_outreach():
    cursor.execute(
        """
        SELECT
            outreach.id,
            outreach.email_subject,
            outreach.email_body,
            leads.contact_email,
            leads.contact_name,
            leads.company_name
        FROM outreach
        JOIN leads ON outreach.lead_id = leads.id
        WHERE outreach.status = 'approved'
    """)
    rows = cursor.fetchall()
    return rows_to_dicts(cursor, rows)

def mark_outreach_sent(outreach_id):
    cursor.execute(
        """
        UPDATE outreach
        SET status = 'sent', sent_at = ?
        WHERE id = ?
    """, (date.today().isoformat(), outreach_id))
    conn.commit()