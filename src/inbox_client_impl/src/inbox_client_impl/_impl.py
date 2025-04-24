
from typing import ClassVar, Optional
from collections.abc import Iterator

from googleapiclient.discovery import build, Resource # type: ignore[import-untyped]
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore[import-untyped]
from google.oauth2.credentials import Credentials

import base64
import os.path
import email  # Needed for sending

# Import the protocol
import inbox_client_protocol
import message

FAILURE_TO_CRED = "Failed to obtain credentials. Please check your setup."

class GmailClient(inbox_client_protocol.Client):
    """Concrete implementation of the Client protocol using Gmail API."""

    SCOPES: ClassVar[list[str]] = [
        "https://www.googleapis.com/auth/gmail.modify"
    ]

    def __init__(self, service: Resource | None = None) -> None: #noqa: PLR0915, PLR0912, C901
        if service:
            self.service = service
            return # Skip auth if service is provided

        creds: Credentials | None = None

        # Check for CircleCI Environment Variables First
        client_id = os.environ.get("GMAIL_CLIENT_ID")
        client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
        refresh_token = os.environ.get("GMAIL_REFRESH_TOKEN")
        token_uri = os.environ.get("GMAIL_TOKEN_URI", "https://oauth2.googleapis.com/token")

        if client_id and client_secret and refresh_token:
            print("Attempting to authenticate using environment variables (CI mode)...")
            try:
                creds = Credentials( # type: ignore[no-untyped-call]
                    None,
                    refresh_token=refresh_token,
                    token_uri=token_uri,
                    client_id=client_id,
                    client_secret=client_secret,
                    scopes=self.SCOPES
                )
                creds.refresh(Request()) # type: ignore[no-untyped-call]
                print("Authentication via environment variables successful.")
            except Exception as e:
                print(f"Error refreshing token from environment variables: {e}")
                creds = None # Ensure creds is None if refresh fails
                raise

        # Fallback to file-based auth if env vars failed or aren't present
        if not creds:
            print("Attempting to authenticate using local files...")
            token_path = "token.json" #noqa: S105
            creds_path = "credentials.json"

            if os.path.exists(token_path): #noqa: PTH110
                try:
                    creds = Credentials.from_authorized_user_file( # type: ignore[no-untyped-call]
                        token_path, self.SCOPES
                    )
                except Exception as e:
                     print(f"Error loading token from {token_path}: {e}")
                     creds = None # Ensure creds is None if loading fails

            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid: # pragma: no cover
                # --- START OF INTERACTIVE BLOCK TO EXCLUDE ---
                if creds and creds.expired and creds.refresh_token: # pragma: no cover
                    print("Refreshing token from file...") # pragma: no cover
                    try:
                        creds.refresh(Request()) # type: ignore[no-untyped-call]
                    except Exception as e: # pragma: no cover
                         print(f"Error refreshing token from file: {e}") # pragma: no cover
                         creds = None # Force re-auth if refresh fails # pragma: no cover
                else: # pragma: no cover
                    # Run the interactive flow only if absolutely necessary
                    print("Running interactive authentication flow...") # pragma: no cover
                    if not os.path.exists(creds_path): #noqa: PTH110 # pragma: no cover
                        # This error should only happen in local dev if file is missing
                        raise FileNotFoundError( #noqa: TRY003 # pragma: no cover
                            f"'{creds_path}' not found. Cannot run interactive auth." #noqa: EM102 # pragma: no cover
                        )
                    try: # pragma: no cover
                        flow = InstalledAppFlow.from_client_secrets_file(
                            creds_path, self.SCOPES
                        )
                        creds = flow.run_local_server(port=0)
                    except Exception as e: # pragma: no cover
                         print(f"Error during interactive auth flow: {e}")
                         raise # Re-raise the exception if interactive flow fails

                if creds: # pragma: no cover
                    try: # pragma: no cover
                        with open(token_path, "w") as token: # pragma: no cover
                            token.write(creds.to_json()) # type: ignore[no-untyped-call]
                        print(f"Credentials saved to {token_path}")
                    except Exception as e: # pragma: no cover
                         print(f"Error saving token to {token_path}: {e}")
                # --- END OF INTERACTIVE BLOCK TO EXCLUDE ---
        if not creds:
             raise RuntimeError(FAILURE_TO_CRED)

        # Build the service object
        try:
            self.service = build("gmail", "v1", credentials=creds)
            print("Gmail service built successfully.")
        except Exception as e:
            print(f"Error building Gmail service: {e}")
            raise # Re-raise the exception


    def get_messages(self) -> Iterator[message.Message]:
        """Fetch messages from Gmail and yields Message instances via factory."""
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
                yield message.get_message(
                    msg_id=msg_summary["id"], raw_data=raw_content
                )

    def send_message(self, to: str, subject: str, body: str) -> bool:
        """Send message using the Gmail API."""
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
            print(f"Error sending message: {e}")
            return False

    def delete_message(self, message_id: str) -> bool:
        """Delete message from Gmail using its ID."""
        try:
            (
                self.service.users()
                .messages()
                .delete(userId="me", id=message_id)
                .execute()
            )
            return True
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")
            return False

    def mark_as_read(self, message_id: str) -> bool:
        """Mark message as read in Gmail by removing the UNREAD label."""
        try:
            # Request body to remove the UNREAD label
            modify_request = {"removeLabelIds": ["UNREAD"]}
            (
                self.service.users()
                .messages()
                .modify(
                    userId="me", id=message_id, body=modify_request
                )
                .execute()
            )
            return True
        except Exception as e:
            print(f"Error marking message {message_id} as read: {e}")
            return False
