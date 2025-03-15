import lime
import lime.lime_tabular
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from lime.lime_tabular import LimeTabularExplainer

xgb_model = joblib.load("model/models/xgboost_model.pkl")
lgb_model = joblib.load("model/models/lightgbm_model.pkl")

data_path = r"C:\Users\harsh\data-pipeline\data\transactions.csv"
data = pd.read_csv(data_path)

data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

X = data.drop(columns=["is_fraud", "transaction_id", "transaction_date"])
y = data["is_fraud"]

X_numeric = X.select_dtypes(include=[np.number])
X_non_numeric = X.select_dtypes(exclude=[np.number])

X_numeric = X_numeric.fillna(X_numeric.mean())

for col in X_non_numeric.columns:
    X_non_numeric[col] = X_non_numeric[col].fillna(X_non_numeric[col].mode()[0])

X = pd.concat([X_numeric, X_non_numeric], axis=1)

label_encoders = {}
for column in X.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    X[column] = label_encoders[column].fit_transform(X[column])

if X.isnull().sum().sum() > 0:
    print("Warning: Data still contains NaN values!")
    print(X.isnull().sum())
else:
    print("No missing values left.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

explainer = LimeTabularExplainer(
    training_data=X_train.values,
    training_labels=y_train.values,
    mode='classification',
    feature_names=X.columns.tolist(),
    class_names=np.unique(y_train),
    discretize_continuous=False
)

idx = 1
instance = X_test.iloc[idx]
instance = pd.DataFrame([instance.values], columns=X.columns)  # Ensure it's a DataFrame with correct columns

def model_predict_proba(instance):
    # Ensure instance is a DataFrame with correct column names
    instance_df = pd.DataFrame(instance, columns=X.columns)
    return model.predict_proba(instance_df)

# Now call explain_instance with wrapped prediction function
explanation = explainer.explain_instance(
    instance.values[0], model_predict_proba, num_features=10
)

# Save the explanation to an HTML file
explanation.save_to_file('lime_explanation.html')
