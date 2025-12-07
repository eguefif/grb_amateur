"""
SMTP client for sending email notifications.

This module provides a simple wrapper around Python's smtplib for sending
email notifications through Fastmail's SMTP service. It's primarily used for
sending user registration confirmation emails.

Environment Variables Required:
    POSTMARK_PASS: Fastmail account password
    POSTMARK_LOGIN: Fastmail account email/login
    SMTP_DOMAIN: SMTP server domain (e.g., smtp.fastmail.com)
    SMTP_PORT: SMTP server port (typically 465 for SSL)
"""

import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SMTPClient:
    """
    SMTP client for sending HTML emails via Fastmail.

    Initializes connection parameters from environment variables and provides
    methods for sending confirmation emails.
    """

    def __init__(self):
        """
        Initialize the SMTP client with credentials from environment variables.

        Raises:
            ValueError: If SMTP_PORT cannot be converted to an integer.
        """
        self.sender = os.getenv("FASTMAIL_LOGIN").strip()
        self.password = os.getenv("FASTMAIL_PASSWORD")
        self.login = os.getenv("FASTMAIL_LOGIN").strip()
        self.smtp_domain = os.getenv("FASTMAIL").strip()
        self.smtp_port = int(os.getenv("FASTMAIL_PORT"))

    def send_email(self, emails: list[str], subject, body):
        """
        Send HTML confirmation emails to multiple recipients.

        Establishes an SSL connection to the SMTP server and sends the same
        email content to all recipients in the list.

        Args:
            emails: List of recipient email addresses.
            subject: Email subject line.
            body: HTML content of the email body.

        Raises:
            smtplib.SMTPException: If authentication or sending fails.
            OSError: If connection to SMTP server fails.
        """
        with SMTP_SSL(self.smtp_domain, port=self.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self.login, self.password)
            for email in emails:
                print(f"Sending email to : {email}")
                message = self._get_message(email, subject, body)
                print(message.as_string())
                smtp.sendmail(self.login, email, message.as_string())

    def _get_message(self, email, subject, body):
        """
        Construct a MIME multipart email message with HTML content.

        Args:
            email: Recipient email address.
            subject: Email subject line.
            body: HTML content for the email body.

        Returns:
            MIMEMultipart: Formatted email message ready to send.
        """
        message = MIMEMultipart()
        message["From"] = self.sender
        print(f"Sending email from : {message['From']}")
        message["To"] = email
        message["Subject"] = subject
        print("Sending message:\n", body)
        message.attach(MIMEText(body, "html"))
        return message


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    smtp = SMTPClient()
    smtp.send_email(["eguefif@gmail.com"], "test", "test")
