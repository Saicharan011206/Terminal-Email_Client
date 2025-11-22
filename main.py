print("Welcome to your email_client!")
import smtplib
import imaplib
def send_email():
    print("Sending email...")
    sender_email = input("Enter your email: ")
    receiver_email = input("Enter recipient email: ")
    password = input("Enter your password:(app password if your using gmail) ")
    subject = input("Enter subject: ")
    body = input("Enter email body: ")
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
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