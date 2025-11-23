import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SMTPClient:
    def __init__(self):
        self.password = os.getenv("FASTMAIL_PASS")
        self.login = os.getenv("FASTMAIL_LOGIN")
        self.smtp_domain = os.getenv("SMTP_DOMAIN")
        self.smtp_port = int(os.getenv("SMTP_PORT"))

    def send_confirmation_email(self, emails: list[str], subject, body):
        with SMTP_SSL(self.smtp_domain, port=self.smtp_port) as smtp:
            smtp.login(self.login, self.password)
            for email in emails:
                print(f"Sending email to : {email}")
                message = self._get_message(email, subject, body)
                smtp.sendmail(self.login, email, message.as_string())

    def _get_message(self, email, subject, body):
        message = MIMEMultipart()
        message["From"] = self.login
        message["To"] = email
        message["Subject"] = subject
        print("Sending message:\n", body)
        message.attach(MIMEText(body, "html"))
        return message
