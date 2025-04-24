from typing import ClassVar, Iterator
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import base64
import os.path
import email # Needed for sending

from inbox_client_protocol import Client
from message import Message 
from message_impl import GmailMessage 

class GmailClient(Client):

    SCOPES: ClassVar[list[str]] = [
        "https://www.googleapis.com/auth/gmail.modify"
    ]

    def __init__(self):
        creds = None
        token_path = 'token.json'
        creds_path = 'credentials.json'
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Ensure credentials.json exists or handle the error
                if not os.path.exists(creds_path):
                     raise FileNotFoundError(
                         f"'{creds_path}' not found. Please download client secrets."
                     )
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        self.service = build('gmail', 'v1', credentials=creds)

    def get_messages(self) -> Iterator[Message]: # Return type is the Protocol
        results = self.service.users().messages().list(userId='me', maxResults=10).execute()
        messages_summary = results.get('messages', [])

        for msg_summary in messages_summary:
            # Fetch raw message data needed by GmailMessage
            msg_data = self.service.users().messages().get(
                userId='me', id=msg_summary['id'], format='raw'
            ).execute()
            raw_content = msg_data.get('raw')
            if raw_content:
                 # Instantiate the concrete implementation
                yield GmailMessage(msg_id=msg_summary['id'], raw_data=raw_content)

    # --- Implement Missing Methods ---
    def send_message(self, to: str, subject: str, body: str) -> bool:
        try:
            message = email.message.EmailMessage()
            message.set_content(body)
            message['To'] = to
            message['Subject'] = subject

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'raw': encoded_message}

            send_result = self.service.users().messages().send(
                userId="me", body=create_message
            ).execute()
            return bool(send_result.get('id')) 
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def delete_message(self, message_id: str) -> bool:
        try:
            self.service.users().messages().delete(userId='me', id=message_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")
            return False

    def mark_as_read(self, message_id: str) -> bool:
        try:
            modify_request = {'removeLabelIds': ['UNREAD']}
            self.service.users().messages().modify(
                userId='me', id=message_id, body=modify_request
            ).execute()
            return True
        except Exception as e:
             # Add proper logging here
            print(f"Error marking message {message_id} as read: {e}")
            return False


def get_client() -> GmailClient: # Return the concrete type here
    return GmailClient()
