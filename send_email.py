import pwinput
import smtplib
from login_utils import get_smtp_server
def send_email(user_email, password):
    print("=== Sending Email ===")
    receiver_email = input("Enter recipient's email address: ").strip()
    subject = input("Enter subject: ")
    # Initial email body entry
    while True:
        print("Enter your email body (type 'END' on a new line to finish):")
        body_lines = []
        while True:
            line = input()
            if line == "END":
                break
            body_lines.append(line)
        body = "\n".join(body_lines)

        # Review and options
        print("\n--- Review your email ---")
        print(f"To: {receiver_email}")
        print(f"Subject: {subject}")
        print("Body:\n------------------")
        print(body)
        print("------------------")
        
        confirm = input("Send this email? [y]es / [e]dit / [n]o: ").strip().lower()
        if confirm == 'y':
            break
        elif confirm == 'e':
            print("You chose to edit your email body.")
            # Loop continues and lets user re-enter the body
        elif confirm == 'n':
            print("Email send canceled.")
            return
        else:
            print("Invalid choice. Please enter y, e, or n.")

    message = f"Subject: {subject}\n\n{body}"

    smtp_server,port=get_smtp_server(user_email)
    if smtp_server is None:
        print("Unsupported email provider.")
        return False
    try:
        with smtplib.SMTP(smtp_server,port,timeout=10) as server:
            server.starttls()
            server.login(user_email, password)
            server.sendmail(user_email, receiver_email, message)
        print("Email sent successfully!")
        return True
    except smtblib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email and password.")
    except smtplib.SMTPConnectError:
        print("Failed to connect to the SMTP server. Please check your internet connection.")
    except smtplib.SMTPRecipientsRefused:
        print("The recipient's email address was refused by the server.")
    except smtplib.SMTPException as e:
        print(f"An SMTP error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False
