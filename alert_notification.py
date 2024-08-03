import smtplib
from email.message import EmailMessage

ADMIN_EMAIL = "admin@example.com"
SMTP_SERVER = "localhost"

def send_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "alert@example.com"
    msg['To'] = ADMIN_EMAIL

    with smtplib.SMTP(SMTP_SERVER) as server:
        server.send_message(msg)

def alert_admin(file_path):
    subject = "Quarantine Alert"
    body = f"An email has been moved to quarantine. File: {file_path}"
    send_alert(subject, body)
