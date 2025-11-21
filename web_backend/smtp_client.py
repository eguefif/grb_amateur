import base64
import time
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
        self.backend_domain = os.getenv("BACKEND_DOMAIN")

    def send_confirmation_email(self, email):
        with SMTP_SSL(self.smtp_domain, port=self.smtp_port) as smtp:
            smtp.login(self.login, self.password)
            message = self._get_message(email)
            print(f"Sending email to : {email}")
            smtp.sendmail(self.login, email, message.as_string())

    def _get_message(self, email):
        message = MIMEMultipart()
        message["From"] = self.login
        message["To"] = email
        message["Subject"] = "Confirm email address"
        body = self._make_body(email)
        print("Sending confirmation message:\n", body)
        message.attach(MIMEText(body, "html"))
        return message

    def _make_body(self, email):
        body = "<html><body>"
        body += "<h2>Hello</h2>"
        body += (
            "<p>Please confirm your email address by going to the following addres</p>"
        )
        body += f'<p><a href="{self.backend_domain}/users/confirm/{email}">Confirmation link</a></p>'
        body += "<p>Emmanuel</p>"
        body += "</body></html>"
        return body


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    client = SMTPClient()
    client.send_confirmation_email("eguefif@fastmail.com")
