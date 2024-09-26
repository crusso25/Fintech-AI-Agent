from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware 
import random
import time
import requests
from datetime import datetime, timedelta

app = FastAPI()

API_URL = 'http://127.0.0.1:8002/fraud_detection'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Function to generate a transaction
def generate_transaction(fraud=False):
    transaction = {
        "TransactionTime": random.uniform(0, 172800), 
        "TransactionAmount": round(random.uniform(1.0, 5000.0), 2),
    }
    for i in range(1, 29):
        if fraud:
            transaction[f'V{i}'] = random.uniform(-10.0, 10.0)
        else:
            transaction[f'V{i}'] = random.uniform(-2.0, 2.0)
    return transaction

# Function to simulate transactions
def simulate_transactions(rate_per_minute=60, duration_minutes=10):
    total_transactions = rate_per_minute * duration_minutes
    fraud_probability = 0.02  # 2% fraudulent transactions

    for _ in range(total_transactions):
        is_fraud = random.random() < fraud_probability
        transaction = generate_transaction(fraud=is_fraud)

        try:
            response = requests.post(API_URL, json=transaction)
            if response.status_code == 200:
                result = response.json()
                print(f"Transaction: {transaction['TransactionAmount']} - {result['prediction']} - Probability: {result.get('probability', 'N/A')}")
            else:
                print(f"Failed to process transaction: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(60 / rate_per_minute)  # Wait before sending the next transaction

# API endpoint to trigger transaction simulation
@app.post("/simulate_transactions")
async def start_simulation(rate_per_minute: int = 60, duration_minutes: int = 10, background_tasks: BackgroundTasks = None):
    background_tasks.add_task(simulate_transactions, rate_per_minute, duration_minutes)
    return {"message": "Transaction simulation started", "rate_per_minute": rate_per_minute, "duration_minutes": duration_minutes}

# Run the server with: uvicorn transaction_simulator_api:app --reload
