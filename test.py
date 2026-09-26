from database import init_outreach_table, save_outreach_draft, get_outreach_draft, get_all_leads, rows_to_dicts, review_pending_outreach, cursor
from outreach import generate_outreach_email, verify_email_grounding


if __name__ == '__main__':
    # init_outreach_table()
    # leads = rows_to_dicts(cursor, get_all_leads())
    # for lead in leads:
    #     subject, body = generate_outreach_email(lead)
    #     save_outreach_draft(lead['id'], subject, body)

    print(get_outreach_draft())