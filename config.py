# fraud_prevention/config.py
import os
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")

# Real-Time Fraud Prevention System Configuration
FRAUD_SCORE_THRESHOLD = float(os.getenv("FRAUD_SCORE_THRESHOLD", 0.8)) # Set fraud score threshold to auto-block transactions above this value
TRANSACTION_TIMEOUT = 30  # Time in seconds to timeout a transaction before marking as suspicious

# Fraud Alerting Configuration
ALERT_CHANNELS = {
    "twilio": {
        "enabled": True,  # Set to True to enable Twilio for alerts
        "account_sid": "your_twilio_account_sid",  # Your Twilio Account SID
        "auth_token": "your_twilio_auth_token",    # Your Twilio Auth Token
        "phone_number": "+1234567890"              # Twilio phone number for sending alerts
    },
    "slack": {
        "enabled": True,  # Set to True to enable Slack for alerts
        "slack_webhook_url": "your_slack_webhook_url"  # Slack Webhook URL for sending fraud alerts
    },
    "email": {
        "enabled": True,  # Set to True to enable email alerts
        "smtp_server": "smtp.gmail.com",  # SMTP server for sending emails
        "smtp_port": 587,  # SMTP server port
        "sender_email": "your_email@example.com",  # Your email address
        "sender_password": "your_email_password",  # Your email account password (consider using environment variables for security)
        "recipient_email": "recipient_email@example.com"  # Email address to receive alerts
    }
}

# Multi-Factor Authentication (MFA) & Biometric Verification
MFA_ENABLED = True  # Enable Multi-Factor Authentication (MFA) for added security
MFA_METHODS = ["sms", "email", "auth_app"]  # Available MFA methods (SMS, email, or auth app)

BIOMETRIC_ENABLED = True  # Enable biometric verification (e.g., face recognition, fingerprint)
BIOMETRIC_METHOD = "face_recognition"  # Define which biometric method to use (e.g., 'face_recognition')

# Fraud Case Management Dashboard Configuration
CASE_MANAGEMENT_DASHBOARD_URL = "http://localhost:5000/dashboard"  # URL to the fraud case management dashboard
CASE_STATUS = ["new", "under_review", "resolved", "rejected"]  # Possible case statuses for fraud cases

# Logging Configuration
LOGGING_ENABLED = True  # Enable logging for fraud prevention system
LOG_FILE_PATH = "./logs/fraud_prevention.log"  # Path to save the logs

# Anomaly Detection Configuration
LOCATION_BASED_ANOMALY_DETECTION_ENABLED = True  # Enable detection of location-based anomalies
ANOMALY_THRESHOLD = 0.5  # Threshold for detecting location-based anomalies (e.g., login from two different continents in a short period)

# Other Configurations
SESSION_TIMEOUT = 60 * 5  # Session timeout in seconds (5 minutes) for user sessions
RETRY_LIMIT = 3  # Retry limit for failed verification attempts (e.g., MFA or biometric verification)
