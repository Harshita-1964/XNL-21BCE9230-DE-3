import pandas as pd
import shap
import joblib  # or pickle if that's how your model is saved

# Load your trained model
model = joblib.load("model/models/xgboost_model.pkl")  # Update the path accordingly

# Load the data
data = pd.read_csv("C:/Users/harsh/data-pipeline/data/features.csv").head(100)

# Drop unnecessary columns (like Unnamed columns or ones not needed for the model)
data = data.drop(columns=[col for col in data.columns if 'Unnamed' in col])

# Check for and drop duplicate merchant_id columns (e.g., 'merchant_id' and 'merchant_id_2', etc.)
merchant_columns = [col for col in data.columns if 'merchant_id' in col]
data = data.drop(columns=merchant_columns)

# Ensure the columns match the model's expected ones
model_columns = model.feature_names_in_  # Now this will work because the model is loaded

# Check for missing and extra columns
missing_columns = [col for col in model_columns if col not in data.columns]
extra_columns = [col for col in data.columns if col not in model_columns]

print("Missing columns:", missing_columns)
print("Extra columns:", extra_columns)

# Add missing columns with default values (e.g., NaN or 0)
for col in missing_columns:
    data[col] = 0  # Or another default value like NaN if preferred

# Add extra columns if necessary and remove them (if they aren't needed)
data = data.drop(columns=extra_columns)

# Align the dataset to match the model's expected columns
data = data[model_columns]  # Only keep the columns the model expects

# Proceed with SHAP explainer (assuming model is already loaded)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(data)

# Create a SHAP summary plot
import matplotlib.pyplot as plt
shap.summary_plot(shap_values, data)

# Save the plot
plt.savefig("model/explainability/shap_summary_plot.png")
