import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def send_notification_email(to_email, username, model_name):
    load_dotenv()
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except (ValueError, TypeError):
        smtp_port = 587
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_email or not smtp_password:
        print("[Email Notifier] SMTP credentials not set in env. Skipping email dispatch.")
        return False

    subject = f"⚡ Your Trained AI Model ({model_name}) is Ready!"
    body = f"""Hi {username},

Great news! The AI model '{model_name}' that you submitted for expert training has been personally reviewed, trained, and patched by our expert. 

The safety breaches and instruction malfunctions have been successfully resolved. Your model is now fully optimized and ready for auditing!

Log in to your AI Auditor platform to run an interactive audit on your new model.

Best regards,
The AI Auditor Support Team
"""

    msg = MIMEMultipart()
    msg['From'] = smtp_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())
        server.quit()
        print(f"[Email Notifier] Notification email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"[Email Notifier] Failed to send email: {e}")
        return False
