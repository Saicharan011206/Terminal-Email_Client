print("Welcome to your email_client!")
from send_email import send_email
import pwinput
print("Please Login to continue.")
def login():
     user_email = input("Enter your email address: ").strip()
     password = pwinput.pwinput(prompt="Enter your app password: ", mask="*")
     return user_email, password
def main_menu(user_email, password):
    while True:
        print("\nMain Menu:")
        print("1. Send Email")
        print("2. Receive Email")
        print("3. Logout")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            send_email(user_email, password)
        elif choice == '2':
            receive_email(user_email, password)
        elif choice == '3':
            print("Logging out...")
            return
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    while True:
        user_email, password = login()
        main_menu(user_email, password)