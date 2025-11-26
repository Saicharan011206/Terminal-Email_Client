import imaplib
import email
from email.header import decode_header
from login_utils import get_smtp_server

def get_imap_server(user_email):
    domain = user_email.lower().split('@')[-1]
    if domain == "gmail.com":
        return "imap.gmail.com"
    elif domain in ("outlook.com", "hotmail.com"):
        return "imap-mail.outlook.com"
    else:
        return None

def clean_text(text):
    if isinstance(text, bytes):
        try:
            return text.decode()
        except UnicodeDecodeError:
            return text.decode('utf-8', errors='ignore')
    return text

def receive_email(user_email, password, mailbox="INBOX", num_emails=5):
    imap_server = get_imap_server(user_email)
    if imap_server is None:
        print("❌ Unsupported email provider for receiving emails.")
        return False

    try:
        print(f"🔄 Connecting to IMAP server: {imap_server}...")
        with imaplib.IMAP4_SSL(imap_server) as mail:
            mail.login(user_email, password)
            status, select_data = mail.select(mailbox)
            if status != 'OK':
                print(f"❌ Failed to open mailbox: {mailbox}")
                return False

            status, data = mail.search(None, "ALL")
            if status != "OK":
                print("❌ Failed to search mailbox for emails.")
                return False

            email_ids = data[0].split()
            if not email_ids:
                print("📭 No emails found.")
                return True

            total_emails = len(email_ids)
            fetch_count = min(num_emails, total_emails)
            print(f"📬 Fetching {fetch_count} of {total_emails} emails from '{mailbox}'...")

            for i in email_ids[-fetch_count:]:
                status, msg_data = mail.fetch(i, "(RFC822)")
                if status != "OK":
                    print(f"⚠️ Could not fetch email with ID {i.decode()}. Skipping.")
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        raw_subject = msg.get("Subject", "No Subject")
                        subject, encoding = decode_header(raw_subject)[0]
                        subject = clean_text(subject)
                        from_ = clean_text(msg.get("From", "Unknown Sender"))

                        print("\n" + "="*60)
                        print(f"From: {from_}")
                        print(f"Subject: {subject}")
                        print("-"*60)

                        # Extract and display plain text body snippet
                        body = None
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True)
                                    break
                        else:
                            body = msg.get_payload(decode=True)

                        if body:
                            body_text = clean_text(body).strip()
                            snippet = body_text[:500].replace('\r\n', '\n')
                            print(f"Body preview:\n{snippet}")
                            if len(body_text) > 500:
                                print("... [truncated]")
                        else:
                            print("[No plain text body content]")
            print("\n✅ Finished fetching emails.")
            return True

    except imaplib.IMAP4.abort:
        print("❌ IMAP connection was aborted unexpectedly. Please try again.")
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")

    return False
