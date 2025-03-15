from kafka import KafkaProducer
import json
import time
from config import KAFKA_SERVER, KAFKA_TOPIC

transactions = [
    {"id": 1, "amount": 100, "type": "credit"},
    {"id": 2, "amount": 50, "type": "debit"},
    {"id": 3, "amount": 200, "type": "credit"},
    {"id": 4, "amount": 300, "type": "debit"}
]

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

for transaction in transactions:
    producer.send(KAFKA_TOPIC, value=transaction)
    print(f"Sent: {transaction}")
    time.sleep(1)

producer.close()
