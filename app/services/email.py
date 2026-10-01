import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME"
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD"
)

SMTP_FROM = os.getenv(
    "SMTP_FROM"
)


def send_email(
    to_email: str,
    subject: str,
    body: str
):

    message = EmailMessage()

    message["From"] = SMTP_FROM
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(body)

    with smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD
        )

        server.send_message(message)