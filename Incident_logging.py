import logging

LOG_FILE = "/home/seed/var/log/email_security.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def log_incident(file_path, message):
    logging.info(f"File: {file_path} - {message}")

# Usage
# log_incident("/path/to/email", "Email moved to quarantine due to keyword filtering")
