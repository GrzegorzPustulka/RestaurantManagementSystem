import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from admin_service.config import settings


class SMTPManager:
    def __init__(self, receiver: str):
        self.sender = settings.sender_email
        self.password = settings.smtp_password.get_secret_value()
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.receiver = receiver

    @staticmethod
    def _load_email_template(file_name: str) -> str:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        template_path = os.path.join(base_dir, "../../email_templates", f"{file_name}")
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()

    def send_email(self, subject: str, file_name: str) -> None:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = self.receiver

        text = self._load_email_template(f"{file_name}.txt")
        html = self._load_email_template(f"{file_name}.html")

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            # for mailhog login and password are not required
            server.sendmail(self.sender, self.receiver, message.as_string())
