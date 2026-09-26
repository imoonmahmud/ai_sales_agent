from database import init_db, add_lead, get_all_leads, load_sample_leads, flatten_lead
from qualification import qualify_lead


if __name__ == '__main__':
    init_db()

    for lead in load_sample_leads():
        flat_lead = flatten_lead(lead)
        lead_with_status = qualify_lead(flat_lead, target_keywords=["technology", "software"], max_employee=250, min_employee=50)
        add_lead(
            flat_lead.get('company_name'),
            flat_lead.get('industry'),
            flat_lead.get('employee_count'),
            flat_lead.get('website'),
            flat_lead.get('source'),
            flat_lead.get('notes'),
            flat_lead.get('contact_name'),
            flat_lead.get('contact_role'),
            flat_lead.get('contact_email'),
            lead_with_status.get('score'),
            lead_with_status.get('status')
        )

    print(get_all_leads())