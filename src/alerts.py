
import os
import smtplib
from email.message import EmailMessage


def send_alert(probability, machine_id="MACHINE_001"):

    if probability < 0.70:
        print("Machine operating normally.")
        return False

    sender = os.getenv("ALERT_EMAIL")
    password = os.getenv("ALERT_EMAIL_PASSWORD")
    receiver = os.getenv("ALERT_RECEIVER")

    if not sender or not password or not receiver:
        print("HIGH FAILURE RISK!")
        print("Email credentials are not configured.")
        return False

    message = EmailMessage()

    message["Subject"] = "URGENT: Machine Failure Risk Alert"
    message["From"] = sender
    message["To"] = receiver

    message.set_content(
        f"""
        PREDICTIVE MAINTENANCE ALERT

        Machine: {machine_id}

        Predicted failure probability:
        {probability * 100:.2f}%

        Risk threshold: 70%

        Recommended action:
        Inspect the machine and schedule maintenance.
        """
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(message)

        print("Email alert sent successfully!")
        return True

    except Exception as error:
        print("Email sending failed:", error)
        return False
