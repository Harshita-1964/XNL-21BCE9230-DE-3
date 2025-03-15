import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL Database
def connect_to_postgres():
    conn = psycopg2.connect(
        dbname="fraud_detection", 
        user="your_user", 
        password="your_password", 
        host="localhost", 
        port="5432"
    )
    return conn

# Create fraud cases table
def create_fraud_table(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS fraud_cases (
        transaction_id UUID PRIMARY KEY,
        amount DECIMAL,
        fraud_score FLOAT,
        status VARCHAR(255),
        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()

# Insert fraud case into the table
def insert_fraud_case(conn, transaction_id, amount, fraud_score, status):
    insert_query = """
    INSERT INTO fraud_cases (transaction_id, amount, fraud_score, status)
    VALUES (%s, %s, %s, %s);
    """
    cursor = conn.cursor()
    cursor.execute(insert_query, (transaction_id, amount, fraud_score, status))
    conn.commit()

# Fetch fraud cases
def fetch_fraud_cases(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fraud_cases")
    rows = cursor.fetchall()
    return rows

if __name__ == '__main__':
    conn = connect_to_postgres()
    create_fraud_table(conn)
    # Example Insert
    insert_fraud_case(conn, '123e4567-e89b-12d3-a456-426614174000', 1000.0, 0.9, 'Blocked')
    # Fetching Fraud Cases
    fraud_cases = fetch_fraud_cases(conn)
    for case in fraud_cases:
        print(case)
