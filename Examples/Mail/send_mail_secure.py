from __future__ import print_function
import pickle
import os.path
import base64
import mimetypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GMailService:
    def __init__(self):
        self.authentificate()

    def authentificate(self):
        """ All stuff for connection on gmail
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=8081)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('gmail', 'v1', credentials=creds)

    def send(self, sender, to, subject, message_text, filePath):
        # Load data of the image
        file = open(filePath, 'rb')
        image = MIMEImage(file.read(), name="PyCam.jpg")
        file.close()

        # Prepare the message
        text = MIMEText(message_text)
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = to
        message.attach(text)
        message.attach(image)

        # Encode to base64
        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_str = b64_bytes.decode()
        raw_msg = {'raw': b64_str}

        # Send the message
        self.service.users().messages().send(userId=sender, body=raw_msg).execute()

    def disconnect(self):
        None

if __name__ == "__main__":
    img_data = open('1.jpg', 'rb').read()

    service = GMailService()
    service.send("malik.fleury@gmail.com", "malik.fleury@he-arc.ch", "Test Python", "Détection du XX.XX.XX a XX:XX", './1.jpg')
    service.disconnect()
