import tensorflow as tf
import numpy as np
import joblib
import pandas as pd
import os  

# Load trained model
model_path = "C:/Users/harsh/data-pipeline/model/models/tf_fraud_model.keras"
model = tf.keras.models.load_model(model_path)

# Load feature names
feature_names_path = "C:/Users/harsh/data-pipeline/model/models/feature_names.pkl"
if not os.path.exists(feature_names_path):
    raise FileNotFoundError(f"Feature names file not found: {feature_names_path}. Ensure you saved it during training.")

feature_names = joblib.load(feature_names_path)

# Function to preprocess input data
def preprocess_input(data):
    df = pd.DataFrame([data], columns=["amount", "is_international", "merchant_id", "transaction_type", "balance"])
    df = pd.get_dummies(df, columns=["merchant_id", "transaction_type"], drop_first=True)

    # Efficiently add missing columns
    missing_cols = set(feature_names) - set(df.columns)
    if missing_cols:
        df = pd.concat([df, pd.DataFrame(0, index=df.index, columns=list(missing_cols))], axis=1)

    df = df[feature_names]  # Ensure correct column order
    return df.values.astype(np.float32)

# Prediction function
def predict(data):
    input_data = preprocess_input(data)
    prediction = model.predict(input_data)
    print("Prediction Output:", prediction)
    return prediction

# Test the function
predict([500, 1, 10, 2, 2000])  
