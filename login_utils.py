import pwinput
import smtplib
from time import sleep

def save_last_user(user_email):
    with open("last_user.txt", "w") as f:
        f.write(user_email)

def load_last_user():
    try:
        with open("last_user.txt") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_smtp_server(user_email):
    domain = user_email.lower().split('@')[-1]
    if domain == "gmail.com":
        return "smtp.gmail.com", 587
    elif domain in ("outlook.com", "hotmail.com"):
        return "smtp.office365.com", 587
    else:
        return None, None

def login(password_only=False, user_email=None, max_attempts=3):
    if password_only:
        if not user_email:
            print("Error: No email provided for password-only login.")
            return None
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            password = pwinput.pwinput(prompt=f"Enter app password for '{user_email}' (type 'cancel' to exit): ", mask="*")
            if password.lower() == "cancel":
                print("Login cancelled by user. Exiting.")
                exit()
            if not password:
                print("⚠️  Password can't be blank. Please try again.")
                continue
            smtp_server, port = get_smtp_server(user_email)
            if not smtp_server:
                print("⚠️  Unsupported email provider. Only Gmail, Outlook, or Hotmail are supported.")
                return None
            try:
                with smtplib.SMTP(smtp_server, port, timeout=10) as server:
                    server.starttls()
                    server.login(user_email, password)
                print("✅ Login successful!\n")
                return password
            except smtplib.SMTPAuthenticationError:
                print("❌ Authentication failed: Invalid app password.")
                if attempts < max_attempts:
                    print(f"Attempts left: {max_attempts - attempts}")
                sleep(1)
            except Exception as e:
                print(f"❌ Login failed due to error: {e}")
                sleep(1)
        print("🚫 Too many failed login attempts. Please try again later.")
        exit()
    else:
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            print("\n--- Login ---")
            user_email = input("Enter your email address:(type 'cancel' to exit) ").strip()
            if user_email.lower() == "cancel":
                print("Login cancelled by user. Exiting.")
                exit()
            if not user_email:
                print("⚠️  Email address can't be blank. Please try again or type 'cancel' to exit.")
                continue
            password = pwinput.pwinput(prompt="Enter your app password (type 'cancel' to exit): ", mask="*")
            if password.lower() == "cancel":
                print("Login cancelled by user. Exiting.")
                exit()
            if not password:
                print("⚠️  Password can't be blank. Please try again.")
                continue
            smtp_server, port = get_smtp_server(user_email)
            if not smtp_server:
                print("⚠️  Unsupported email provider. Only Gmail, Outlook, or Hotmail are supported.")
                continue
            if smtp_server == "smtp.gmail.com":
                print("ℹ️  Tip: For Gmail, generate an 'App Password' at https://myaccount.google.com/security.")
            try:
                with smtplib.SMTP(smtp_server, port, timeout=10) as server:
                    server.starttls()
                    server.login(user_email, password)
                print("✅ Login successful!\n")
                return user_email, password
            except smtplib.SMTPAuthenticationError:
                print("❌ Authentication failed: Invalid email or app password.")
                if attempts < max_attempts:
                    print(f"Attempts left: {max_attempts - attempts}")
                sleep(1)
            except Exception as e:
                print(f"❌ Login failed due to error: {e}")
                sleep(1)
        print("🚫 Too many failed login attempts. Please try again later.")
        exit()
