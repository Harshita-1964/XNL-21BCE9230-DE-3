import joblib
import pandas as pd
import sys, os
import logging

# Adding parent directory to the path so that config can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import fraud threshold from config.py
from config import FRAUD_SCORE_THRESHOLD  

# Setup logging for better tracking in production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the pre-trained model (ensure the path is correct)
model = joblib.load("model/models/xgboost_model.pkl")

def apply_dynamic_rules(transaction_data):
    """
    Apply dynamic rules to adjust fraud score threshold.
    """
    dynamic_threshold = FRAUD_SCORE_THRESHOLD
    
    # Example rule: Lower the threshold for international transactions
    if transaction_data['is_international'].iloc[0] == 1:
        dynamic_threshold -= 0.1  # Lower threshold for international transactions
    
    # Example rule: Higher threshold for VIP customers
    if transaction_data['customer_category'].iloc[0] == 1:
        dynamic_threshold += 0.1  # Raise threshold for VIP customers

    # Log the dynamic threshold
    logger.info(f"Dynamic Fraud Score Threshold: {dynamic_threshold}")

    # Add more rules as needed (e.g., based on merchant category or transaction type)

    return dynamic_threshold

def check_fraud(transaction_data):
    """
    Check if a transaction is fraudulent based on the model's prediction probability.
    """
    # Apply dynamic rules to adjust the threshold
    dynamic_threshold = apply_dynamic_rules(transaction_data)
    
    # One-hot encode categorical columns based on the training features
    transaction_data_transformed = pd.get_dummies(transaction_data, 
                                                  columns=['merchant_id', 'transaction_type', 
                                                           'customer_category', 'merchant_category', 
                                                           'card_type', 'day_of_week'])

    # Ensure the features match the model's feature names (from training)
    transaction_data_transformed = transaction_data_transformed.reindex(columns=model.get_booster().feature_names, 
                                                                        fill_value=0)
    
    # Get the fraud score (probability of class 1, which is fraud)
    fraud_score = model.predict_proba(transaction_data_transformed)[0][1]

    # Log the fraud score
    logger.info(f"Fraud score for transaction: {fraud_score}")

    if fraud_score > dynamic_threshold:
        logger.warning(f"Transaction is flagged as fraudulent with score {fraud_score} (Threshold: {dynamic_threshold})")
        return True  # Fraudulent transaction
    else:
        logger.info(f"Transaction is safe with score {fraud_score} (Threshold: {dynamic_threshold})")
        return False  # Safe transaction


# Example transaction for testing
new_transaction = pd.DataFrame([{
    'amount': 1000,
    'merchant_id': 123,
    'is_international': 1,
    'day_of_week': 4,  # Monday is 0, Tuesday is 1, ..., Sunday is 6
    'is_weekend': 0,
    'high_amount_flag': 1,
    'transaction_type': 0,  # 0 = Online, 1 = POS (or whatever encoding you used)
    'customer_category': 2,  # 0 = Regular, 1 = VIP, etc.
    'merchant_category': 1,  # Fashion, Grocery, etc.
    'card_type': 1  # 0 = Debit, 1 = Prepaid, etc.
}])

# Ensure the correct columns (matching the model's training features)
expected_columns = [
    'amount', 'merchant_id', 'is_international', 'day_of_week', 
    'is_weekend', 'high_amount_flag', 'transaction_type', 
    'customer_category', 'merchant_category', 'card_type'
]

# Reorder or ensure the features are aligned properly
new_transaction = new_transaction[expected_columns]

# Print the model's feature names to compare
booster = model.get_booster()
features = booster.feature_names
logger.info("Model features: %s", features)

# Call the check_fraud function with the transaction data
check_fraud(new_transaction)
