print("Welcome to your email_client!")
from send_email import send_email
def receive_email():
    print("Receiving email...")
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Send Email")
        print("2. Receive Email")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            send_email()
        elif choice == '2':
            receive_email()
        elif choice == '3':
            print("Exiting email_client. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main_menu()