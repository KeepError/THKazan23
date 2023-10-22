import smtplib
from email.mime.text import MIMEText

from src.settings import settings


def send_mail(recipients: list[str], subject: str, text: str):
    sent_from = settings.mail_login

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ', '.join(recipients)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(settings.mail_login, settings.mail_password)
    server.sendmail(sent_from, recipients, msg.as_string())
    server.close()
