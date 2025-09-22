import os
import pandas as pd
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURATION VIA ENV VARIABLES ---
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.google.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))
EMAIL_FROM = os.environ.get("EMAIL_FROM", "testpython@test.com")
EMAIL_TO = os.environ.get("EMAIL_TO", "sejiy98569@bitfami.com")

# --- 1. Fetch Report Data ---
def fetch_data():
    # Replace this with your actual data source (SQL, Mongo, Redash, etc.)
    return [
        ["Metric 1", 100],
        ["Metric 2", 200],
        ["Metric 3", 300],
    ]

# --- 2. Generate Excel Report ---
def generate_excel_report(data):
    filename = "report.xlsx"
    df = pd.DataFrame(data, columns=["Metric", "Value"])
    df.to_excel(filename, index=False)
    return filename

# --- 3. Send Email with Attachment (MIME, No Auth) ---
def send_email_with_attachment(subject, body, to_email, attachment_path):
    try:
        # Create MIME message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add plain text body
        msg.attach(MIMEText(body, 'plain'))

        # Attach the file
        with open(attachment_path, "rb") as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
            msg.attach(part)

        # Send via SMTP (no login)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()

        print("Email with attachment sent successfully (no auth).")

    except Exception as e:
        logging.error(f"Email sending failed: {e}")
        raise

# --- 4. Main Function: Generate Report + Send Email ---
def generate_and_send_report():
    try:
        data = fetch_data()
        report_filename = generate_excel_report(data)

        subject = "Daily Report - Sent via Unauthenticated SMTP"
        body = (
            "Hello,\n\n"
            "Please find the attached daily report.\n\n"
            "This email was sent using an SMTP relay that does not require login."
        )

        send_email_with_attachment(subject, body, EMAIL_TO, report_filename)

    except Exception as e:
        logging.error(f"Failed to generate and send report: {e}")
        raise
