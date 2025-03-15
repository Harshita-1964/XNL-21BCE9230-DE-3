from locust import HttpUser, task, between

class FraudDetectionTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_fraud_detection(self):
        self.client.post("/api/fraud_data", json={
            'amount': 5000,
            'merchant_id': '123',
            'is_international': False,
            'customer_category': 'VIP'
        })

    @task
    def test_fraud_trends(self):
        self.client.get("/api/fraud_trends")
