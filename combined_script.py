import os
import shutil
import email
from email.policy import default
import smtplib
from email.message import EmailMessage
import logging

# Define keywords to filter
FILTER_KEYWORDS = ["update your account", "click here", "create an account", "login now"]

# Paths
INBOX_DIR = "/home/seed/var/mail/inbox"
QUARANTINE_DIR = "/home/seed/var/mail/quarantine"
LOG_FILE = "/home/seed/var/mail/email_security.log"

# Admin email for alerts
ADMIN_EMAIL = "seed@localhost.com"
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
    msg['From'] = "seed@localhost.com"
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


