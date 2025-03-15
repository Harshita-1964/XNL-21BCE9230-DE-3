from google.cloud import bigquery
from google.oauth2 import service_account

# Authenticate and Connect to BigQuery
def connect_to_bigquery():
    credentials = service_account.Credentials.from_service_account_file('path_to_your_service_account_key.json')
    client = bigquery.Client(credentials=credentials, project='your_project_id')
    return client

# Create table for storing fraud cases
def create_fraud_table(client):
    dataset_id = 'your_dataset_id'
    table_id = f'{dataset_id}.fraud_cases'
    
    schema = [
        bigquery.SchemaField("transaction_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("amount", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("fraud_score", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    ]
    
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

# Insert fraud case into the table
def insert_fraud_case(client, transaction_id, amount, fraud_score, status):
    dataset_id = 'your_dataset_id'
    table_id = f'{dataset_id}.fraud_cases'
    
    rows_to_insert = [
        {"transaction_id": transaction_id, "amount": amount, "fraud_score": fraud_score, "status": status, "timestamp": 'CURRENT_TIMESTAMP'}
    ]
    
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New fraud case inserted successfully.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")

if __name__ == '__main__':
    client = connect_to_bigquery()
    create_fraud_table(client)
    # Example Insert
    insert_fraud_case(client, '123e4567-e89b-12d3-a456-426614174000', 1000.0, 0.9, 'Blocked')
