import smtplib
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(client, barber, receivers):

    html = f"""
        <h2>Olá {barber}!</h2>
        <p>Um <strong>novo serviço</strong> foi adicionado na sua agenda.</p>
        <p><a href="https://calendar.google.com">Clique aqui para ver</a>.</p>
        """

    if isinstance(receivers, str):
        receivers = [receivers]

    msg = MIMEText(html, 'html')  # Corpo como HTML
    msg['Subject'] = f'{client} agendou pelo baber app!'
    msg['From'] = EMAIL_FROM
    msg['To'] = COMMASPACE.join(receivers)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_FROM, receivers, msg.as_string())