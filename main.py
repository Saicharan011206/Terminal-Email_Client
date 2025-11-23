print("Welcome to your email_client!")
from login_utils import login, save_last_user, load_last_user
from send_email import send_email
# from receive_email import receive_email  # Uncomment when implemented.
import sys

def main_menu(user_email, password):
    while True:
        print(f"\nMain Menu (Logged in as: {user_email})")
        print("1. Send Email")
        print("2. Receive Email")
        print("3. Logout and Login as Another User")
        print("4. Logout and Exit Program")
        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':
            try:
                send_email(user_email, password)
            except Exception as e:
                print(f"❌ Error sending email: {e}")
        elif choice == '2':
            try:
                receive_email(user_email, password)  # Implement and import this if needed.
            except Exception as e:
                print(f"❌ Error receiving email: {e}")
        elif choice == '3':
            print("Logging out... Returning to login screen.")
            return 'return_to_login'
        elif choice == '4':
            save_last_user(user_email)
            print("Exiting the program. Goodbye!")
            sys.exit()
        else:
            print("⚠️ Invalid choice. Please enter 1, 2, 3, or 4.")

def prompt_last_login():
    last_email = load_last_user()
    if last_email:
        print(f"\n👋 Welcome back! Last logged in account: {last_email}")
        use_last = input("Login with this account? (y/n): ").strip().lower()
        if use_last == 'y':
            password = login(password_only=True, email=last_email)
            return last_email, password
        elif use_last == 'n':
            return login()
        else:
            print("⚠️ Invalid choice. Proceeding to login screen.")
            return login()
    else:
        return login()

if __name__ == "__main__":
    while True:
        print("Please log in to continue.")
        user_email, password = prompt_last_login()
        action = main_menu(user_email, password)
        if action == 'return_to_login':
            continue
        break

