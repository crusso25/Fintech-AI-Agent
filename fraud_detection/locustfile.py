from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta

locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
merchant_types = ['Electronics', 'Groceries', 'Clothing', 'Restaurants', 'Travel']
spending_habits = ['Low', 'Moderate', 'High']

def generate_transaction(fraud=False):
    transaction = {
        "TransactionAmount": round(random.uniform(10.0, 500.0), 2),
        "TransactionTime": (datetime.now() - timedelta(seconds=random.randint(0, 86400))).isoformat(),
        "Location": random.choice(locations),
        "MerchantType": random.choice(merchant_types),
        "Age": random.randint(18, 70),
        "Income": round(random.uniform(30000, 150000), 2),
        "SpendingHabits": random.choice(spending_habits)
    }

    if fraud:
        transaction['TransactionAmount'] = round(random.uniform(1000.0, 10000.0), 2)
        transaction['Location'] = 'Unknown'
        transaction['MerchantType'] = 'Luxury Items'
        transaction['SpendingHabits'] = 'Very High'

    return transaction

class FraudDetectionUser(HttpUser):
    wait_time = between(0.1, 0.5)  # Wait between requests

    @task
    def send_transaction(self):
        fraud_probability = 0.02
        is_fraud = random.random() < fraud_probability
        transaction = generate_transaction(fraud=is_fraud)
        self.client.post("/predict", json=transaction)
