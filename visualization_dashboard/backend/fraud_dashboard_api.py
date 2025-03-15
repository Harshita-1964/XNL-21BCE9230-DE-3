from flask import Flask, jsonify
from cassandra.cluster import Cluster

app = Flask(__name__)

# Connect to Cassandra
def connect_to_cassandra():
    cluster = Cluster(['localhost'])  # replace with your Cassandra node IP
    session = cluster.connect('fraud_detection')  # Replace with your keyspace
    return session

# Fetch fraud data
@app.route('/api/fraud_data', methods=['GET'])
def get_fraud_data():
    session = connect_to_cassandra()
    fetch_query = "SELECT * FROM fraud_cases"
    rows = session.execute(fetch_query)
    fraud_cases = [{"transaction_id": row.transaction_id, "amount": row.amount, 
                    "fraud_score": row.fraud_score, "status": row.status} for row in rows]
    return jsonify(fraud_cases)

# Fetch fraud trends
@app.route('/api/fraud_trends', methods=['GET'])
def get_fraud_trends():
    session = connect_to_cassandra()
    fetch_query = "SELECT date, fraud_cases_count FROM fraud_trends"
    rows = session.execute(fetch_query)
    trends = [{"date": row.date, "fraud_cases_count": row.fraud_cases_count} for row in rows]
    return jsonify(trends)

if __name__ == '__main__':
    app.run(debug=True)
