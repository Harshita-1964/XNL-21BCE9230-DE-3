import pandas as pd
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fraud_prevention.real_time_fraud_prevention import check_fraud
from fraud_prevention.config import FRAUD_SCORE_THRESHOLD
from fraud_prevention.fraud_alerting import send_fraud_alerts

def test_normal_transaction():
    new_transaction = pd.DataFrame([{
        'amount': 1000,
        'merchant_id': 123,
        'is_international': 1,
        'day_of_week': 4,
        'is_weekend': 0,
        'high_amount_flag': 1,
        'transaction_type': 0,
        'customer_category': 2,
        'merchant_category': 1,
        'card_type': 1
    }])
    print("Testing Normal Transaction:")
    check_fraud(new_transaction)
def test_high_risk_transaction():
    new_transaction = pd.DataFrame([{
        'amount': 5000,
        'merchant_id': 456,
        'is_international': 1,
        'day_of_week': 2,
        'is_weekend': 0,
        'high_amount_flag': 1,
        'transaction_type': 1,
        'customer_category': 1,
        'merchant_category': 2,
        'card_type': 0
    }])
    print("Testing High-Risk Transaction:")
    check_fraud(new_transaction)

def test_low_risk_transaction():
    new_transaction = pd.DataFrame([{
        'amount': 50,
        'merchant_id': 789,
        'is_international': 0,
        'day_of_week': 5,
        'is_weekend': 1,
        'high_amount_flag': 0,
        'transaction_type': 0,
        'customer_category': 3,
        'merchant_category': 3,
        'card_type': 1
    }])
    print("Testing Low-Risk Transaction:")
    check_fraud(new_transaction)

@patch('fraud_prevention.fraud_alerting.send_twilio_alert')
@patch('fraud_prevention.fraud_alerting.send_slack_alert')
@patch('fraud_prevention.fraud_alerting.send_email_alert')
def test_send_fraud_alerts(mock_send_sms, mock_send_slack, mock_send_email):
    fraud_score = 0.85
    transaction_id = "TX123456789"

    send_fraud_alerts(fraud_score, transaction_id)

    
    mock_send_sms.assert_called_once_with("+1234567890", f"Fraud alert! Transaction ID {transaction_id} has a fraud score of {fraud_score}.")
    mock_send_slack.assert_called_once_with(config.SLACK_WEBHOOK_URL, f"Fraud alert! Transaction ID {transaction_id} has a fraud score of {fraud_score}.")
    mock_send_email.assert_called_once_with(config.EMAIL_ADDRESS, "Fraud Alert", f"Fraud alert! Transaction ID {transaction_id} has a fraud score of {fraud_score}.")

if __name__ == "__main__":
    print(f"Current Fraud Threshold: {FRAUD_SCORE_THRESHOLD}")
    test_normal_transaction()
    test_high_risk_transaction()
    test_low_risk_transaction()
    test_send_fraud_alerts()  
