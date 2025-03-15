from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Connect to Cassandra Cluster
def connect_to_cassandra():
    cluster = Cluster(['localhost'])  # replace with your Cassandra node IP
    session = cluster.connect('fraud_detection')  # Replace with your keyspace
    return session

# Create a table to store fraud transaction data
def create_fraud_table(session):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS fraud_cases (
        transaction_id UUID PRIMARY KEY,
        amount DECIMAL,
        fraud_score FLOAT,
        status TEXT,
        timestamp TIMESTAMP
    );
    """
    session.execute(create_table_query)

# Insert fraud case data into the table
def insert_fraud_case(session, transaction_id, amount, fraud_score, status):
    insert_query = """
    INSERT INTO fraud_cases (transaction_id, amount, fraud_score, status, timestamp)
    VALUES (%s, %s, %s, %s, toTimestamp(now()));
    """
    session.execute(insert_query, (transaction_id, amount, fraud_score, status))

# Fetch fraud cases
def fetch_fraud_cases(session):
    fetch_query = "SELECT * FROM fraud_cases"
    rows = session.execute(fetch_query)
    return rows

if __name__ == '__main__':
    session = connect_to_cassandra()
    create_fraud_table(session)
    # Example Insert
    insert_fraud_case(session, '123e4567-e89b-12d3-a456-426614174000', 1000.0, 0.9, 'Blocked')
    # Fetching Fraud Cases
    fraud_cases = fetch_fraud_cases(session)
    for case in fraud_cases:
        print(case)
