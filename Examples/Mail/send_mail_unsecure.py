import os
import smtplib

from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# GMAIL : Need to enable "Insecure access".

class MailService:
    def __init__(self, user, password, address, port):
        smtp_server = smtplib.SMTP_SSL(address, port)
        smtp_server.login(user, password)
        self.smtp_server = smtp_server

    def send(self, subject, mail_from, mail_to, txt, img_data):
        image = MIMEImage(img_data, name="PyCam")
        text = MIMEText(txt)
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = mail_from
        message['To'] = mail_to
        message.attach(text)
        message.attach(image)
        self.smtp_server.send_message(message)

    def disconnect(self):
        self.smtp_server.quit()

if __name__ == "__main__":
    img_data = open('1.jpg', 'rb').read()

    service = MailService('smtp.gmail.com', 465, "MAIL", "PASSWORD")
    service.send("Test Python", "MAIL", "MAIL", "Détection du XX.XX.XX a XX:XX", img_data)
    service.disconnect()
