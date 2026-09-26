import time
from database import get_approved_outreach, mark_outreach_sent, get_pending_outreach, get_outreach_draft
from email_sender import send_email

def send_approved_emails():
    approved = get_approved_outreach()

    if not approved:
        print("No approved emails to sent")
        return

    for item in approved:
        print(f"Sending to {item['contact_name']} at {item['company_name']} ({item['contact_email']})...")
        success = send_email(
            to_address=item['contact_email'],
            subject=item['email_subject'],
            body=item['email_body'])
        if success:
            mark_outreach_sent(item['id'])
            print(f"Send and marked")
        else:
            print("Failed - left as 'approved' for retry.")
        time.sleep(5)



if __name__ == '__main__':
    # send_approved_emails()
    pending = get_outreach_draft()
    for lead in pending:
        print(lead, '\n')