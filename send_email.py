import pwinput
import smtplib
def send_email():
    print("=== Sending Email ===")
    sender_email = input("Enter your email address: ").strip()
    receiver_email = input("Enter recipient's email address: ").strip()
    password = pwinput.pwinput(prompt="Enter your app password: ", mask="*")
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

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
