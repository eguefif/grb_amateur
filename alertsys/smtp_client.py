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

    def send_emails(self, email_lists, alert):
        with SMTP_SSL(self.smtp_domain, port=self.smtp_port) as smtp:
            smtp.login(self.login, self.password)
            message = self._get_message(alert)
            for email in email_lists:
                print(f"Sending email to : {email}")
                message["To"] = email
                smtp.sendmail(self.login, email, message.as_string())
                time.sleep(2)

    def _get_message(self, alert):
        message = MIMEMultipart()
        message["From"] = self.login
        message["Subject"] = "Fermi GRB alert"
        body = self._make_body(alert)
        print("Sending alert message:\n", body)
        message.attach(MIMEText(body, "plain"))
        return message

    def _make_body(self, alert):
        body = "This a alert from GRB alert and observation\n"
        body += "A Gamma Ray Burst has been detected by the Fermi salettlie"
        body += "Notice date: " + alert["notice_date"] + "\n"
        body += "Comments: " + alert["comments"] + "\n"
        body += "\nEnjoy\n"
        body += "Emmanuel"
        return body
