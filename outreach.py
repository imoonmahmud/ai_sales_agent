import unicodedata
from llm import ask_llm
from database import get_all_leads

def normalize_text(text):
    return unicodedata.normalize('NFKC', text)

def generate_outreach_email(lead):
    known_fact = []

    if lead.get('industry') and lead['industry'] != 'unknown':
        known_fact.append(f"Industry:  {lead['industry']}")
    if lead.get('employee_count'):
        known_fact.append(f"Company size approximately {lead['employee_count']} employees")
    if lead.get('notes'):
        known_fact.append(f"Additional info: {lead['notes']}")

    facts_text = '\n'.join(known_fact) if known_fact else 'No specific company details available'

    prompt = f"""Write a short, professional cold outreach email.
        Recipient: {lead['contact_name']}, {lead['contact_role']} at {lead['company_name']}

        STRICT RULES:
        - Use ONLY the facts listed below. Do not mention anything about this
        company or person that is not explicitly listed.
        - Do not invent names, founders, funding, products, achievements, or
        any other detail not given.
        - Do not claim any personal connection, prior conversation, shared
        contact, or event attendance that isn't stated below.
        - If you have very few facts, write a shorter, more generic-but-honest
        email rather than inventing details to fill space.
        - Address {lead['contact_name']} by name, and reference their role
        ({lead['contact_role']}) naturally if relevant.

        KNOWN FACTS ABOUT {lead['company_name']}:
        {facts_text}

        Write the email now. Keep it under 100 words. Sign it as "Alex, Sales Team".
        """
    
    email = ask_llm(prompt)
    first_line = email.splitlines()[0]
    subject = first_line.split(':', 1)[1].strip()

    body = email.split('\n', 1)[1].strip()

    return subject, body

def verify_email_grounding(email_text, lead):
    flags = []
    email_lower = normalize_text(email_text).lower()
    company_name_normalized = normalize_text(lead['company_name']).lower()

    suspicious_terms = [
        'founded by', 'raised', 'series a', 'series b', 'series c',
        'funding round', 'ipo', 'recently launched', 'award-winning',
        'as we discussed', 'great meeting you', 'following up on our call']

    for term in suspicious_terms:
        if term in email_lower:
            flags.append(f"Contains potentially fabricated claim: '{term}'")

    if lead['contact_name'].split()[0].lower() not in email_lower:
        flags.append(f"Email doesn't seem to address {lead['contact_name']} by name")
    if company_name_normalized not in email_lower:
        flags.append(f"Email doesn't mention the company name '{lead['company_name']}'")

    return flags

