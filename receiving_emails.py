import imaplib
import email
from email.header import decode_header
from login_utils import get_smtp_server

def get_imap_server(user_email):
    domain = user_email.lower().split('@')[-1]
    if domain == 'gmail.com':
        return 'imap.gmail.com'
    elif domain in ('hotmail.com', 'outlook.com'):
        return 'imap-mail.outlook.com'
    else:
        return None

def clean_text(text):
    if isinstance(text, bytes):
        try:
            text = text.decode()
        except UnicodeDecodeError:
            text = text.decode('utf-8', errors='ignore')
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
            status, data = mail.search(None, 'ALL')
            if status != 'OK':
                print("❌ Failed to search emails.")
                return False
            email_ids = data[0].split()
            if not email_ids:
                print("📭 No emails found.")
                return True
            total_emails = len(email_ids)
            print(f"📬 Total emails in {mailbox}: {total_emails}")
            fetch_count = min(num_emails, total_emails)
            print(f"📥 Fetching the latest {fetch_count} emails...\n")
            for i in email_ids[-fetch_count:]:
                status, msg_data = mail.fetch(i, '(RFC822)')
                if status != 'OK':
                    print(f"❌ Failed to fetch email ID: {i.decode()}")
                    continue
                msg = email.message_from_bytes(msg_data[0][1])
                # Decode Subject
                raw_subject = msg.get("Subject", "No Subject")
                subj, encoding = decode_header(raw_subject)[0]
                if isinstance(subj, bytes):
                    subj = subj.decode(encoding if encoding else 'utf-8', errors='ignore')
                # Decode From
                raw_from = msg.get("From", "Unknown Sender")
                from_, encoding2 = decode_header(raw_from)[0]
                if isinstance(from_, bytes):
                    from_ = from_.decode(encoding2 if encoding2 else 'utf-8', errors='ignore')
                print(f"---\nFrom: {clean_text(from_)}\nSubject: {clean_text(subj)}")
                # Process email content
                if msg.is_multipart():
                    for part in msg.walk():
                        c_type = part.get_content_type()
                        c_dispo = str(part.get('Content-Disposition'))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            body = ""
                        if c_type == 'text/plain' and 'attachment' not in c_dispo:
                            print(f"Body:\n{clean_text(body)}")
                            break
                else:
                    c_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if c_type == 'text/plain':
                        print(f"Body:\n{clean_text(body)}")
        print("✅ Done fetching emails.")
        return True
    except imaplib.IMAP4.abort:
        print("❌ IMAP connection was aborted unexpectedly. Please try again.")
        return False
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP error: {e}")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False
    return False




