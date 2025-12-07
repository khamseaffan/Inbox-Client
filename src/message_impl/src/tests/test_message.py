# src/message_impl/src/tests/test_message_impl.py
import base64
from typing import Optional
import pytest
from email.message import Message as EmailMessage
import email.utils # Import email.utils

# Import the class we are testing
from message_impl._impl import GmailMessage

# --- Test Data Fixtures ---

VALUE_EXCEPTION = "create_raw_data helper cannot directly create multipart bodies. Use create_multipart_raw_data." # noqa: E501

def create_raw_data( #noqa: PLR0913
    subject: str = "Test Subject",
    from_addr: str = "sender@example.com",
    to_addr: str = "recipient@example.com",
    date_str: str = "Thu, 24 Apr 2025 10:00:00 +0000",
    body: str = "This is the body.",
    content_type: str = 'text/plain; charset="utf-8"',
    extra_headers: dict[str, str] | None = None,
) -> str:
    """Return a base64 encoded raw email message."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = date_str
    if extra_headers:
        for k, v in extra_headers.items():
            msg[k] = v

    # --- FIX: More robust charset handling and payload setting ---
    if content_type and content_type.startswith("multipart"):
        # This helper is simplified, real multipart needs attach()
        # Set a default payload or raise error if used incorrectly
        # For now, let's assume it won't be used directly for multipart
         raise ValueError(VALUE_EXCEPTION)
    # Determine charset
    charset = "utf-8" # Default
    if content_type and "charset=" in content_type:
        potential_charset = content_type.split("charset=")[-1].strip('" ')
        # Basic check if charset seems valid, otherwise default
        try:
             body.encode(potential_charset) # Test encoding
             charset = potential_charset
        except LookupError:
             print(f"Warning: Unknown charset '{potential_charset}', using utf-8.")
             charset = "utf-8"

    msg.set_payload(body.encode(charset))
    if content_type:
        msg["Content-Type"] = content_type
    else:
         # Default content type if none provided
         msg["Content-Type"] = f'text/plain; charset="{charset}"'
    # --- END FIX ---

    return base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")


# create_multipart_raw_data remains the same as it was likely correct

def create_multipart_raw_data( #noqa: PLR0913
    subject: str="Multipart Test",
    from_addr: str="sender@example.com",
    to_addr: str="recipient@example.com",
    date_str: str="Thu, 24 Apr 2025 11:00:00 +0000",
    text_body: str="This is the plain text part.",
    html_body: str="<p>This is the HTML part.</p>",
) -> str:
    """Return helper for basic multipart/alternative."""
    outer = EmailMessage()
    outer["Subject"] = subject
    outer["From"] = from_addr
    outer["To"] = to_addr
    outer["Date"] = date_str

    part1 = EmailMessage()
    part1.set_payload(text_body.encode("utf-8"))
    part1.set_charset("utf-8") # Good practice to set charset on part
    outer.attach(part1)

    part2 = EmailMessage()
    part2.set_payload(html_body.encode("utf-8"))
    part2.set_charset("utf-8")
    # Set content type explicitly for HTML part
    part2.add_header("Content-Type", "text/html", charset="utf-8")
    outer.attach(part2)

    return base64.urlsafe_b64encode(outer.as_bytes()).decode("utf-8")



# --- Tests (remain the same) ---
# ... (rest of the test functions as before) ...

def test_gmailmessage_basic_parsing() -> None:
    """Test basic property access after initialization."""
    msg_id = "id_1"
    raw = create_raw_data()
    gm = GmailMessage(msg_id, raw)

    assert gm.id == msg_id
    assert gm.subject == "Test Subject"
    assert gm.from_ == "sender@example.com"
    assert gm.to == "recipient@example.com"
    assert gm.date == "04/24/2025" # Check formatting
    assert gm.body == "This is the body."

def test_gmailmessage_missing_headers() -> None:
    """Test properties when headers are missing."""
    msg_id = "id_missing"
    # Create data with minimal structure, missing common headers
    raw_minimal = base64.urlsafe_b64encode(b"Minimal body").decode("utf-8")
    gm = GmailMessage(msg_id, raw_minimal)

    assert gm.id == msg_id
    assert gm.subject == "" # Should default to empty
    assert gm.from_ == ""
    assert gm.to == ""
    assert gm.date == "Unknown Date" # Default fallback
    assert gm.body == "Minimal body" # Body should still parse

def test_gmailmessage_date_parsing() -> None:
    """Test date formatting and fallback."""
    gm_valid = GmailMessage("id_date1", create_raw_data(date_str="Fri, 25 Apr 2025 15:30:10 -0400"))
    assert gm_valid.date == "04/25/2025"

    gm_invalid_format = GmailMessage("id_date2", create_raw_data(date_str="Invalid Date String"))
    assert gm_invalid_format.date == "Invalid Date String" # Fallback

    gm_no_date = GmailMessage("id_date3", create_raw_data(date_str=""))
    assert gm_no_date.date == "Unknown Date" # Fallback for empty

def test_gmailmessage_subject_decoding() -> None:
    """Test decoding of RFC 2047 encoded subjects."""
    encoded_subject = "=?utf-8?q?Encoded_Subject_Test?="
    raw = create_raw_data(subject=encoded_subject)
    gm = GmailMessage("id_subj1", raw)
    assert gm.subject == "Encoded Subject Test"

    plain_subject = "Plain Subject"
    raw_plain = create_raw_data(subject=plain_subject)
    gm_plain = GmailMessage("id_subj2", raw_plain)
    assert gm_plain.subject == plain_subject
