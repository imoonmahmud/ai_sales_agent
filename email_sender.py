import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(to_address, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'imoonmahmud@gmail.com'
    msg['To'] = to_address

    try:
        with smtplib.SMTP(os.getenv('MAILTRAP_HOST'), int(os.getenv('MAILTRAP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('MAILTRAP_USERNAME'), os.getenv('MAILTRAP_PASSWORD'))
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
