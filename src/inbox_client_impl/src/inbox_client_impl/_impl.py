from typing import ClassVar, Iterator
from datetime import datetime
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
import os.path
import inbox_client_api
import message
import logging
from src.message_impl.src.message_impl._impl import GmailMessage

class GmailClient(inbox_client_api.Client):
    SCOPES: ClassVar[list[str]] = ["https://www.googleapis.com/auth/gmail.readonly"]

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

        for msg_summary in messages:
            msg_id = msg_summary['id']
            # Fetch the full message including raw data
            msg_data = self.service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
            raw_email_data = msg_data.get('raw') # Get the 'raw' field
            if raw_email_data:
                 yield GmailMessage(msg_id=msg_id, raw_data=raw_email_data)
            else:
                 logging.warning(f"Raw data missing for message ID {msg_id}, skipping.")
    def send_message(self, to, body) -> bool:
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = 'No Subject'
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            message_body = {'raw': raw}
            self.service.users().messages().send(userId='me', body=message_body).execute()
            return True
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            return False
    
    def delete_message(self, message_id) -> bool:
        try:
            self.service.users().messages().delete(userId='me', id=message_id).execute()
            return True
        except Exception as e:
            logging.error(f"Failed to delete message {message_id}: {e}")
            return False
    def mark_as_read(self, message_id) -> bool:
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            logging.error(f"Failed to mark message {message_id} as read: {e}")
            return False

    
def get_client() -> GmailClient:
    return GmailClient()

    
    