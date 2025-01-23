import smtplib
from datetime import datetime
from zoneinfo import ZoneInfo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from conf.secrets import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SENDER_EMAIL,
    RECEIVER_EMAIL,
)


class EmailException(Exception):
    """
    Custom exception for email-related errors.
    """

    pass


def send_email(email_body: str):
    """
    Sends an email with the specified HTML body.

    The function creates an email with the current date in the subject line and sends it
    using the SMTP server credentials provided in the configuration.

    :param email_body: The HTML content of the email body.
    :raises EmailException: If there is an error while sending the email.
    """
    subject = f"News Alert - {datetime.now(tz=ZoneInfo('America/New_York')).strftime('%b %d, %Y')}"

    # Create the email
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = subject
    message.attach(MIMEText(email_body, "html"))  # Attach the HTML body

    server = None
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()  # Upgrade the connection to secure (TLS)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)  # Log in to the SMTP server

        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())

    except Exception as e:
        raise EmailException(f"Failed to send email: {e}")

    finally:
        # Close the connection
        if server:
            server.quit()
