from getpass import getpass
import smtplib
def send_email():
    print("Sending email...")
    sender_email = input("Enter your email: ")
    receiver_email = input("Enter recipient email: ")
    password = getpass("Enter your password:(app password if your using gmail) ")
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