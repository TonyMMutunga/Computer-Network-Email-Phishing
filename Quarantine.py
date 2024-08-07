import os

QUARANTINE_DIR = "/home/seed/var/mail/quarantine"

def list_quarantined_emails():
    return os.listdir(QUARANTINE_DIR)

def release_email(filename):
    # Implement logic to release email from quarantine if required
    pass

def delete_email(filename):
    file_path = os.path.join(QUARANTINE_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        log_incident(file_path, "Email deleted from quarantine")

if __name__ == "__main__":
    print("Quarantined Emails:")
    for email in list_quarantined_emails():
        print(email)
