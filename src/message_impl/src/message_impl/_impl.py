import base64
import email
from email.message import Message as EmailMessage
from datetime import datetime

# Import the protocol
import message

class GmailMessage(message.Message):
    """Concrete implementation of the Message protocol for Gmail."""

    def __init__(self, msg_id: str, raw_data: str):
        """
        Initializes a GmailMessage instance.

        Args:
            msg_id: The unique ID of the Gmail message.
            raw_data: The raw, base64url encoded email data.

        """
        self._id = msg_id
        self._raw_data = raw_data
        # Decode the raw data and parse it into an EmailMessage object
        try:
            decoded_bytes = base64.urlsafe_b64decode(raw_data.encode("utf-8"))
            self._parsed: EmailMessage = email.message_from_bytes(
                decoded_bytes
            )
        except (TypeError, ValueError, Exception) as e:
            # Handle potential decoding or parsing errors gracefully
            print(f"Error parsing message {msg_id}: {e}")
            # Create a dummy EmailMessage to avoid subsequent attribute errors
            self._parsed = EmailMessage()
            self._parsed["Subject"] = "Error Parsing Message"
            self._parsed["From"] = "Unknown Sender"
            self._parsed["To"] = "Unknown Recipient"
            self._parsed["Date"] = "Unknown Date"

    @property
    def id(self) -> str:
        """Returns the unique message ID."""
        return self._id

    @property
    def from_(self) -> str:
        """Returns the sender's email address, or empty string if not found."""
        return self._parsed.get("From", "")

    @property
    def to(self) -> str:
        """Returns the recipient's email address, or empty string if not found."""
        return self._parsed.get("To", "")

    @property
    def date(self) -> str:
        """
        Returns the message date formatted as MM/DD/YYYY,
        or the raw date string if parsing fails.
        """
        raw_date = self._parsed.get("Date", "")
        if not raw_date:
            return "Unknown Date"
        try:
            # Attempt to parse the date string into a datetime object
            parsed_dt = email.utils.parsedate_to_datetime(raw_date)
            # Format the datetime object
            return parsed_dt.strftime("%m/%d/%Y")
        except (TypeError, ValueError, Exception):
            # Fallback to the raw date string if parsing fails
            return raw_date

    @property
    def subject(self) -> str:
        """Returns the message subject, or empty string if not found."""
        # Decode header potentially containing encoded words (RFC 2047)
        subject_header = self._parsed.get("Subject", "")
        if not subject_header:
            return ""
        decoded_parts = email.header.decode_header(subject_header)
        subject_str = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                # If it's bytes, decode using the specified encoding or default
                subject_str += part.decode(encoding or "utf-8", errors="replace")
            else:
                # If it's already a string, just append
                subject_str += part
        return subject_str

    @property
    def body(self) -> str:
        """
        Extracts and returns the plain text body of the message.
        Walks through multipart messages to find the text/plain part.
        """
        body_content = ""
        if self._parsed.is_multipart():
            for part in self._parsed.walk():
                content_type = part.get_content_type()
                content_disposition = part.get("Content-Disposition", "")

                # Look for plain text parts that are not attachments
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        # Decode payload, handling potential encoding issues
                        payload = part.get_payload(decode=True)
                        if isinstance(payload, bytes):
                            charset = part.get_content_charset() or "utf-8"
                            body_content = payload.decode(charset, errors="replace")
                            # Found the plain text body, no need to look further
                            break
                        # Handle non-bytes payload if necessary, maybe it's already text?
                        # Or log a warning/error
                        body_content = "[Non-bytes payload found in text/plain part]"
                        break
                    except Exception as e:
                        print(f"Error decoding part for message {self.id}: {e}")
                        body_content = "[Could not decode body part]"
                        break
            else:
                # If no text/plain part found after walking
                body_content = "[No plain text body found]"
        else:
            # If it's not multipart, get the main payload
            try:
                payload = self._parsed.get_payload(decode=True)
                if isinstance(payload, bytes):
                    charset = self._parsed.get_content_charset() or "utf-8"
                    body_content = payload.decode(charset, errors="replace")
                else:
                    # Handle non-bytes payload
                    body_content = "[Non-bytes payload found]"
            except Exception as e:
                print(f"Error decoding payload for message {self.id}: {e}")
                body_content = "[Could not decode body]"

        return body_content
