from src.crawler import crawl_mailbox

def test_crawl_mailbox():
    emails = crawl_mailbox()
    assert isinstance(emails, list)
    assert all('mail_id' in email and 'body' in email for email in emails)
    assert len(emails) > 0