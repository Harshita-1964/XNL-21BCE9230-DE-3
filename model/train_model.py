import pandas as pd
import xgboost as xgb
import lightgbm as lgb
import torch
import torch.nn as nn
import tensorflow as tf
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE

# Ensure model directory exists
os.makedirs("model/models", exist_ok=True)

# Load dataset
data = pd.read_csv("C:/Users/harsh/data-pipeline/data/transactions.csv")

# Fix date parsing issue
data['transaction_date'] = pd.to_datetime(data['transaction_date'], format="%d-%m-%Y", errors='coerce')

# Drop unwanted columns
data.drop(columns=['transaction_date', 'transaction_id'], inplace=True)

# Forward fill missing values to fix warning
data.ffill(inplace=True)

# Ensure categorical columns are converted properly
data = pd.get_dummies(data, columns=["merchant_id", "transaction_type", "customer_category", "merchant_category", "card_type", "day_of_week"], drop_first=True)

# Fill remaining NaNs with zero to avoid SMOTE errors
data.fillna(0, inplace=True)

# Ensure all numeric columns
data["is_international"] = data["is_international"].astype(int)

# Fix feature names for LightGBM compatibility
data.columns = data.columns.str.replace(r'[^a-zA-Z0-9_]', '_', regex=True)

# Separate features and target
X = data.drop(columns=["is_fraud"])
y = data["is_fraud"]

# Apply SMOTE after ensuring all features are numeric
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)
joblib.dump(list(X_train.columns), "model/models/feature_names.pkl")

# Train XGBoost model
xgb_model = xgb.XGBClassifier(enable_categorical=False, tree_method="hist")
xgb_model.fit(X_train, y_train)

# Train LightGBM model
lgb_model = lgb.LGBMClassifier()
lgb_model.fit(X_train, y_train)

# Predictions and accuracy
xgb_preds = xgb_model.predict(X_test)
lgb_preds = lgb_model.predict(X_test)

print("XGBoost Accuracy:", accuracy_score(y_test, xgb_preds))
print("LightGBM Accuracy:", accuracy_score(y_test, lgb_preds))

# Save models
joblib.dump(xgb_model, "model/models/xgboost_model.pkl")
joblib.dump(lgb_model, "model/models/lightgbm_model.pkl")

# ================== PyTorch Model ====================
class FraudDetector(nn.Module):
    def __init__(self, input_size):
        super(FraudDetector, self).__init__()
        self.fc = nn.Linear(input_size, 1)

    def forward(self, x):
        x = self.fc(x.float())  # Ensure correct dtype
        return torch.sigmoid(x)

# Initialize PyTorch model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch_model = FraudDetector(X_train.shape[1]).to(device)

# Save the model structure and state
torch.save({
    'model_state_dict': torch_model.state_dict(),
    'input_size': X_train.shape[1]
}, "model/models/torch_fraud_model.pth")

# ================== TensorFlow Model ====================
tf_model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

tf_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train TensorFlow model
tf_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Save the TensorFlow model correctly
tf_model.save("C:/Users/harsh/data-pipeline/model/models/tf_fraud_model.keras")

print("✅ All models trained and saved successfully!")
