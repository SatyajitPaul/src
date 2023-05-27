import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_email(email: str, access_token: str):
    # Replace with your email sending logic
    sender_email = "your-email@example.com"
    receiver_email = email
    subject = "Email Confirmation"
    body = f"Please click the following link to confirm your email: <a href='{access_token}'>Confirm Email</a>"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the HTML version of the email
    html_message = MIMEText(body, "html")
    message.attach(html_message)

    # Send the email using SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, "your-password")
        server.sendmail(sender_email, receiver_email, message.as_string())