from typing import ClassVar, Iterator
from datetime import datetime
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from email.message import EmailMessage
from inbox_client_impl.constants import GMAIL_SCOPES
import base64
import os.path
import inbox_client_api
import message

class GmailClient(inbox_client_api.Client):
    # SCOPES: ClassVar[list[str]] = ["https://www.googleapis.com/auth/gmail.readonly"]
    SCOPES: ClassVar[list[str]] = GMAIL_SCOPES

    def __init__(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_messages(self) -> Iterator[message.Message]:
        results = self.service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])

        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
            yield message.Message(msg_data)

    def send(self, message: EmailMessage):
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': encoded_message}
        self.service.users().messages().send(userId='me', body=body).execute()

    def delete(self, message_id: str):
        self.service.users().messages().delete(userId='me', id=message_id).execute()

    def mark_as_read(self, message_id: str):
        self.service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

def get_client() -> GmailClient:
    return GmailClient()

    
    