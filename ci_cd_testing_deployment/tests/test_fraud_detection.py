import pytest
from fraud_prevention.real_time_fraud_prevention import detect_fraud

# Test fraud detection function
def test_detect_fraud():
    # Sample data
    test_data = {
        'amount': 5000,
        'merchant_id': '123',
        'is_international': False,
        'customer_category': 'VIP',
    }
    
    # Assuming detect_fraud function returns True for fraud
    assert detect_fraud(test_data) is True
