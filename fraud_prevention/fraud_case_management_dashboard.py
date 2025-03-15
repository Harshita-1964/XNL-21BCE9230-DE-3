from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy  # Optional if connecting to a database

app = Flask(__name__)
# Optional: configure SQLAlchemy or other databases if necessary
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fraud_cases.db'
# db = SQLAlchemy(app)

# Sample fraud case data (replace with real data fetching logic)
fraud_cases = [
    {"transaction_id": "12345", "fraud_score": 0.9, "status": "Blocked"},
    {"transaction_id": "12346", "fraud_score": 0.7, "status": "Safe"},
    {"transaction_id": "12347", "fraud_score": 0.8, "status": "Blocked"},
    {"transaction_id": "12348", "fraud_score": 0.4, "status": "Safe"},
]

@app.route('/')
def home():
    # Optionally fetch fraud cases from the database
    # fraud_cases = db.session.query(FraudCase).all()
    return render_template('index.html', fraud_cases=fraud_cases)

if __name__ == '__main__':
    app.run(debug=True)
