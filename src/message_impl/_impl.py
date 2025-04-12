import base64
import email
from email.message import Message as EmailMessage
from datetime import datetime
import message  


class GmailMessage(message.Message):
    def __init__(self, msg_id: str, raw_data: str):
        self._id = msg_id
        self._raw_data = raw_data
        self._parsed: EmailMessage = email.message_from_bytes(
            base64.urlsafe_b64decode(raw_data.encode('utf-8'))
        )

    @property
    def id(self) -> str:
        return self._id

    @property
    def from_(self) -> str:
        return self._parsed["From"] or ""

    @property
    def to(self) -> str:
        return self._parsed["To"] or ""

    @property
    def date(self) -> str:
        raw_date = self._parsed["Date"]
        try:
            parsed = email.utils.parsedate_to_datetime(raw_date)
            return parsed.strftime("%m/%d/%Y")
        except Exception:
            return raw_date  # fallback

    @property
    def subject(self) -> str:
        return self._parsed["Subject"] or ""

    @property
    def body(self) -> str:
        if self._parsed.is_multipart():
            for part in self._parsed.walk():
                if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                    return part.get_payload(decode=True).decode(errors="replace")
        return self._parsed.get_payload(decode=True).decode(errors="replace")