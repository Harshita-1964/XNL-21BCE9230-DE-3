import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import os

# Load and preprocess data
data = pd.read_csv(r"C:\Users\harsh\data-pipeline\data\features.csv")

# Drop rows with missing target variable 'transaction_type' (if applicable)
X = data.drop(columns=["transaction_type"])  # Drop the target column
y = data["transaction_type"]  # Set the target to transaction_type

# Ensure all missing values in features are filled with 0
X.fillna(0, inplace=True)

# One-hot encode categorical columns (like day_of_week, customer_category, merchant_category, and card_type)
categorical_columns = ['day_of_week', 'customer_category', 'merchant_category', 'card_type']
X = pd.get_dummies(X, columns=categorical_columns, drop_first=True)

# Convert features to float32 for TensorFlow
X = X.astype('float32')

# Encode the target variable (if it’s categorical)
y = pd.get_dummies(y)

# Split the data into train and test sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define the neural network model
model = keras.Sequential([
    layers.Input(shape=(X_train.shape[1],)),  # Use Input layer for the first layer
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(y_train.shape[1], activation='softmax')  # Softmax for multi-class classification
])

# Compile the model with Adam optimizer and categorical crossentropy for multi-class classification
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Evaluate the model on the test set
loss, acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {acc:.4f}")

# Ensure the directory exists before saving the model
save_dir = "../models"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Save the trained model in .keras format
model.save(os.path.join(save_dir, "tf_transaction_type_model.keras"))
