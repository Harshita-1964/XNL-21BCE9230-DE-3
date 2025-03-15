from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os

app = FastAPI()

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "xgboost_model.pkl")
model = joblib.load(os.path.abspath(MODEL_PATH))

# Expected feature names
EXPECTED_FEATURES = [
    "amount", "is_international", "is_weekend", "high_amount_flag",
    *[f"merchant_id_{i}" for i in range(2, 101)],
    "transaction_type_Online", "transaction_type_POS",
    "customer_category_Regular", "customer_category_VIP",
    "merchant_category_Fashion", "merchant_category_Grocery", "merchant_category_Travel",
    "card_type_Debit", "card_type_Prepaid",
    "day_of_week_Monday", "day_of_week_Saturday", "day_of_week_Sunday",
    "day_of_week_Thursday", "day_of_week_Tuesday", "day_of_week_Wednesday"
]

@app.post("/predict/")
async def predict(data: dict):
    try:
        df = pd.DataFrame([data])
        print("Received input:\n", df)

        # Handle merchant_id one-hot encoding
        merchant_id_cols = {f"merchant_id_{i}": 0 for i in range(2, 101)}
        if "merchant_id" in df.columns:
            merchant_id = df["merchant_id"].iloc[0]
            if 2 <= merchant_id <= 100:
                merchant_id_cols[f"merchant_id_{merchant_id}"] = 1
            df.drop(columns=["merchant_id"], inplace=True)  # Remove original column

        # One-hot encoding for categorical columns
        categorical_cols = ["transaction_type", "customer_category", "merchant_category", "card_type"]
        df = pd.get_dummies(df, columns=categorical_cols, prefix=categorical_cols)

        # Add missing expected columns using `pd.concat()`
        missing_cols = {col: 0 for col in EXPECTED_FEATURES if col not in df.columns}
        df = pd.concat([df, pd.DataFrame([missing_cols])], axis=1)

        # Ensure correct feature order
        df = df[EXPECTED_FEATURES]

        print("Final input shape:", df.shape)  # Debugging

        # Predict
        prediction = model.predict(df)[0]
        return {"is_fraud": int(prediction)}

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
