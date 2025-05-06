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

    def __init__(self, service: Resource | None = None, interactive: bool = False) -> None: #noqa: PLR0915, PLR0912, C901, FBT001, FBT002
        """Initialize the GmailClient, handling authentication.

        Args:
            service: An optional pre-configured Google API service resource.
            interactive: If True, force interactive login, ignoring env vars and token.json.

        """
        if service:
            self.service = service
            return # Skip auth if service is provided

        creds: Credentials | None = None
        token_path = "token.json" #noqa: S105
        creds_path = "credentials.json"

        # --- Authentication Logic --- #

        # 1. Force Interactive Flow if requested
        if interactive:
            print("Interactive login requested, skipping environment variables and token file.")
            creds = self._run_interactive_flow(creds_path)

        # 2. Try Environment Variables (CI Mode) if not interactive
        if not creds and not interactive:
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
                    # Don't raise here, allow fallback to file/interactive

        # 3. Try Token File if not interactive and env vars failed
        if not creds and not interactive:
            print("Attempting to authenticate using local token file...")
            if os.path.exists(token_path):
                try:
                    creds = Credentials.from_authorized_user_file( # type: ignore[no-untyped-call]
                        token_path, self.SCOPES
                    )
                    # Check if token needs refresh
                    if creds and not creds.valid and creds.refresh_token:
                        print("Refreshing token from file...")
                        try:
                            creds.refresh(Request()) # type: ignore[no-untyped-call]
                        except Exception as e:
                            print(f"Error refreshing token from file: {e}")
                            creds = None # Force re-auth if refresh fails
                except Exception as e:
                     print(f"Error loading token from {token_path}: {e}")
                     creds = None # Ensure creds is None if loading fails

        # 4. Fallback to Interactive Flow if all else fails (and not already done)
        if not creds or (creds and not creds.valid and not creds.refresh_token):
            if not interactive: # Only run if not explicitly forced earlier
                print("No valid credentials found, falling back to interactive login.")
                creds = self._run_interactive_flow(creds_path)
            elif not creds: # If interactive was forced but failed
                 raise RuntimeError("Interactive authentication failed.") #noqa: EM101 TRY003

        # --- End Authentication Logic --- #

        if not creds or not creds.valid:
             raise RuntimeError(FAILURE_TO_CRED)

        # Save the token if it was obtained interactively or refreshed
        if interactive or (creds.refresh_token and not os.path.exists(token_path)):
             self._save_token(creds, token_path)

        # Build the service object
        try:
            self.service = build("gmail", "v1", credentials=creds)
            print("Gmail service built successfully.")
        except Exception as e:
            print(f"Error building Gmail service: {e}")
            raise # Re-raise the exception

    def _run_interactive_flow(self, creds_path: str) -> Credentials | None:
        """Run the interactive OAuth flow."""
        print("Running interactive authentication flow...")
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"'{creds_path}' not found. Cannot run interactive auth.") #noqa: EM102 TRY003
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, self.SCOPES
            )
            return flow.run_local_server(port=0) # type: ignore[no-any-return]
        except Exception as e:
             print(f"Error during interactive auth flow: {e}")
             return None # Return None on failure

    def _save_token(self, creds: Credentials, token_path: str) -> None:
        """Save the credentials token to a file."""
        try:
            with open(token_path, "w") as token:
                token.write(creds.to_json()) # type: ignore[no-untyped-call]
            print(f"Credentials saved to {token_path}")
        except Exception as e:
             print(f"Error saving token to {token_path}: {e}")

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
