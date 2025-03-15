import torch
import torch.nn as nn

# Define the model class
class FraudDetector(nn.Module):
    def __init__(self, input_size=121):  # Set input_size to match the checkpoint's model
        super(FraudDetector, self).__init__()
        self.fc = nn.Linear(input_size, 1)  # Update input size to match checkpoint (121)

    def forward(self, x):
        return torch.sigmoid(self.fc(x))  # Sigmoid activation for binary classification

# Load the model with additional meta-data
model_path = r"C:\Users\harsh\data-pipeline\model\models\torch_fraud_model.pth"
checkpoint = torch.load(model_path)

# If the checkpoint contains a state_dict, extract it and load it into the model
if 'model_state_dict' in checkpoint:
    model = FraudDetector(input_size=121)  # Match the input size with the checkpoint
    model.load_state_dict(checkpoint['model_state_dict'])  # Load state_dict into the model
else:
    model.load_state_dict(checkpoint)  # Load directly if no extra meta-data

model.eval()  # Set the model to evaluation mode

# Function to make predictions
def predict_fraud(input_data):
    # Convert input data to tensor
    input_tensor = torch.tensor(input_data, dtype=torch.float32)
    
    # Make the prediction
    prediction = model(input_tensor)

    # Convert prediction to 0 or 1 (fraud or not fraud)
    fraud_class = (prediction.item() > 0.5)  # Threshold of 0.5 for binary classification

    # Return fraud status
    return fraud_class

# Example input data with 121 features (5 original features + 116 padding)
example_data = [[500, 1, 0, 1, 2000] + [0]*116]  # Adjusted to match 121 features

# Get the prediction
fraud_class = predict_fraud(example_data)

# Output the prediction
if fraud_class:
    print("Fraud Prediction: 1 (Fraudulent)")
else:
    print("Fraud Prediction: 0 (Non-Fraudulent)")
