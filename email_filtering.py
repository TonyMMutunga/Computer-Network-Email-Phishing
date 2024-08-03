import os
import shutil
import email
from email.policy import default

# Define keywords to filter
FILTER_KEYWORDS = ["phishing", "malware", "virus"]

# Paths
INBOX_DIR = "/var/mail/inbox"
QUARANTINE_DIR = "/var/mail/quarantine"

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

def process_inbox():
    for filename in os.listdir(INBOX_DIR):
        file_path = os.path.join(INBOX_DIR, filename)
        filter_email(file_path)

if __name__ == "__main__":
    process_inbox()
