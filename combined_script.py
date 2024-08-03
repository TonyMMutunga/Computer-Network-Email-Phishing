import os
import shutil
import email
from email.policy import default
import smtplib
from email.message import EmailMessage
import logging

# Define keywords to filter
FILTER_KEYWORDS = ["phishing", "malware", "virus"]

# Paths
INBOX_DIR = "/var/mail/inbox"
QUARANTINE_DIR = "/var/mail/quarantine"
LOG_FILE = "/var/log/email_security.log"

# Admin email for alerts
ADMIN_EMAIL = "admin@example.com"
SMTP_SERVER = "localhost"

# Logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def filter_email(file_path):
    with open(file_path, 'r') as f:
        msg = email.message_from_file(f, policy=default)
    if any(keyword in msg.get_payload(decode=True).decode('utf-8', 'ignore').lower() for keyword in FILTER_KEYWORDS):
        quarantine_email(file_path)

def quarantine_email(file_path):
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    shutil.move(file_path, os.path.join(QUARANTINE_DIR, os.path.basename(file_path)))
    log_incident(file_path, "Email moved to quarantine due to keyword filtering")
    alert_admin(file_path)

def log_incident(file_path, message):
    logging.info(f"File: {file_path} - {message}")

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

def process_inbox():
    for filename in os.listdir(INBOX_DIR):
        file_path = os.path.join(INBOX_DIR, filename)
        filter_email(file_path)

if __name__ == "__main__":
    process_inbox()
