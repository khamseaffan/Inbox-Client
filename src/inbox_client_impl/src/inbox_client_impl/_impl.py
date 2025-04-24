from typing import ClassVar, Iterator, Optional # Added Optional
from googleapiclient.discovery import build, Resource
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import base64
import os.path
import email  # Needed for sending

# Import the protocol
import inbox_client_protocol
import message


class GmailClient(inbox_client_protocol.Client):
    """Concrete implementation of the Client protocol using Gmail API."""

    SCOPES: ClassVar[list[str]] = [
        "https://www.googleapis.com/auth/gmail.modify"
    ]

    def __init__(self, service: Optional[Resource] = None):
        if service:
            self.service = service
        else:
            # Only perform auth flow if service wasn't provided
            creds = None
            token_path = "token.json"
            creds_path = "credentials.json"

            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(
                    token_path, self.SCOPES
                )
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(creds_path):
                        raise FileNotFoundError(
                            f"'{creds_path}' not found. Please download client secrets."
                        )
                    flow = InstalledAppFlow.from_client_secrets_file(
                        creds_path, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                with open(token_path, "w") as token:
                    token.write(creds.to_json())
            self.service = build("gmail", "v1", credentials=creds)


    def get_messages(self) -> Iterator[message.Message]:
        """Fetches messages from Gmail and yields Message instances via factory."""
        results = (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=10)
            .execute()
        )
        messages_summary = results.get("messages", [])

        for msg_summary in messages_summary:
            # Fetch raw message data needed by GmailMessage
            msg_data = (
                self.service.users()
                .messages()
                .get(userId="me", id=msg_summary["id"], format="raw")
                .execute()
            )
            raw_content = msg_data.get("raw")
            if raw_content:
                # Use the factory function from the message protocol package
                # The implementation's __init__ ensures this calls get_message_impl
                yield message.get_message(
                    msg_id=msg_summary["id"], raw_data=raw_content
                )

    def send_message(self, to: str, subject: str, body: str) -> bool:
        """Sends an email using the Gmail API."""
        try:
            email_msg = email.message.EmailMessage()
            email_msg.set_content(body)
            email_msg["To"] = to
            email_msg["Subject"] = subject

            encoded_message = base64.urlsafe_b64encode(
                email_msg.as_bytes()
            ).decode()
            create_message = {"raw": encoded_message}

            send_result = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            # Check if the send operation returned an ID, indicating success
            return bool(send_result.get("id"))
        except Exception as e:
            # Basic error logging, consider using a proper logger
            print(f"Error sending message: {e}")
            return False

    def delete_message(self, message_id: str) -> bool:
        """Deletes a message from Gmail using its ID."""
        try:
            self.service.users().messages().delete(
                userId="me", id=message_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")
            return False

    def mark_as_read(self, message_id: str) -> bool:
        """Marks a message as read in Gmail by removing the UNREAD label."""
        try:
            # Request body to remove the UNREAD label
            modify_request = {"removeLabelIds": ["UNREAD"]}
            self.service.users().messages().modify(
                userId="me", id=message_id, body=modify_request
            ).execute()
            return True
        except Exception as e:
            print(f"Error marking message {message_id} as read: {e}")
            return False

def get_client() -> inbox_client_protocol.Client:
    """
    Factory function returning an instance of the concrete GmailClient.

    Returns:
        inbox_client_protocol.Client: An instance of GmailClient conforming to the protocol.
    """
    return GmailClient()