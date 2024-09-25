import requests
import random
import time
from datetime import datetime, timedelta

API_URL = 'http://127.0.0.1:8000/predict'

def generate_transaction(fraud=False):
    transaction = {
        "TransactionTime": random.uniform(0, 172800), 
        "TransactionAmount": round(random.uniform(1.0, 5000.0), 2),
    }
    # Generate random values for V1 to V28
    for i in range(1, 29):
        if fraud:
            # Generate values more likely to be considered fraudulent
            transaction[f'V{i}'] = random.uniform(-10.0, 10.0)
        else:
            # Generate normal transaction values
            transaction[f'V{i}'] = random.uniform(-2.0, 2.0)
    return transaction

def simulate_transactions(rate_per_minute=60, duration_minutes=10):
    total_transactions = rate_per_minute * duration_minutes
    fraud_probability = 0.02  # 2% transactions are fraudulent

    for _ in range(total_transactions):
        is_fraud = random.random() < fraud_probability
        transaction = generate_transaction(fraud=is_fraud)

        # Send transaction to API
        try:
            response = requests.post(API_URL, json=transaction)
            if response.status_code == 200:
                result = response.json()
                print(f"Transaction: {transaction['TransactionAmount']} - {result['prediction']} - Probability: {result.get('probability', 'N/A')}")
            else:
                print(f"Failed to process transaction: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

        # Wait before sending the next transaction
        time.sleep(60 / rate_per_minute)  # Convert rate per minute to interval in seconds

if __name__ == '__main__':
    simulate_transactions(rate_per_minute=120, duration_minutes=5)
