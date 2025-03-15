# A/B testing script for fraud detection models
from model.train_model import XGBoostModel
from model.train_tf_model import TensorFlowModel

def run_ab_test():
    model_a = XGBoostModel()
    model_b = TensorFlowModel()
    
    # Simulate testing data
    test_data = [
        {'amount': 1000, 'merchant_id': '123', 'is_international': True},
        {'amount': 5000, 'merchant_id': '456', 'is_international': False},
    ]
    
    # Compare the results of two models
    a_results = [model_a.predict(data) for data in test_data]
    b_results = [model_b.predict(data) for data in test_data]
    
    # Evaluate performance of each model
    print("Model A results:", a_results)
    print("Model B results:", b_results)
