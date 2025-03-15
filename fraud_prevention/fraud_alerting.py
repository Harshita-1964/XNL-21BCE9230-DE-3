from twilio.rest import Client
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

# Twilio setup for SMS
def send_twilio_alert(to_phone, message):
    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    twilio_phone_number = config.TWILIO_PHONE_NUMBER

    message = client.messages.create(
        to=to_phone,
        from_=twilio_phone_number,
        body=message
    )
    print(f"Twilio alert sent: {message.sid}")

# Slack setup for messages
def send_slack_alert(slack_webhook_url, message):
    payload = {'text': message}
    response = requests.post(slack_webhook_url, json=payload)
    print(f"Slack alert sent: {response.status_code}")

# Email alert
def send_email_alert(to_email, subject, message):
    from_email = config.EMAIL_ADDRESS
    password = config.EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
    print(f"Email alert sent to {to_email}")

# Example usage of the fraud alert functions
def send_fraud_alerts(fraud_score, transaction_id):
    message = f"Fraud alert! Transaction ID {transaction_id} has a fraud score of {fraud_score}."
    send_twilio_alert(config.RECIPIENT_PHONE_NUMBER, message)
    send_slack_alert(config.SLACK_WEBHOOK_URL, message)
    send_email_alert(config.EMAIL_ADDRESS, "Fraud Alert", message)

# Example usage:
send_fraud_alerts(0.85, "TX123456789")
