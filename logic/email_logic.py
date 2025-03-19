from flask import url_for
from config import config
from email.message import EmailMessage
import smtplib
import ssl


def _send_email(message: EmailMessage):
    with smtplib.SMTP_SSL(
        "smtp.gmail.com", 465, context=ssl.create_default_context()
    ) as server:
        server.login(config.GMAIL_ADDRESS, config.GMAIL_PASSWORD)
        server.send_message(message)


def send_email_to_writer(segment_uid: str, to_email: str) -> None:
    msg = EmailMessage()
    msg.set_content(
        f"You can find your poem at "
        f"{url_for('webapp.segment', segment_uid=segment_uid, _external=True)}"
    )
    msg["Subject"] = "Track your poem here!"
    msg["From"] = config.GMAIL_ADDRESS
    msg["To"] = to_email

    _send_email(msg)


def send_email_to_next(segment_uid: str, to_email: str):
    msg = EmailMessage()
    msg.set_content(
        f"You've been added to contribute to a poem here: "
        f"{url_for('webapp.segment', segment_uid=segment_uid, _external=True)}"
    )
    msg["Subject"] = "Help write a poem!"
    msg["From"] = config.GMAIL_ADDRESS
    msg["To"] = to_email

    _send_email(msg)
