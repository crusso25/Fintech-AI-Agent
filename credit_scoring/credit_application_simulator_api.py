from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware 
import random
import time
import requests
from datetime import datetime, timedelta

app = FastAPI()

API_URL = 'http://127.0.0.1:8002/credit_scoring'  # Send to integration API

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Function to generate a credit application
def generate_credit_application():
    application = {
        "person_age": random.randint(18, 70),
        "person_income": round(random.uniform(15000.0, 200000.0), 2),
        "person_emp_length": round(random.uniform(0.0, 40.0), 1),
        "loan_amnt": round(random.uniform(1000.0, 50000.0), 2),
        "loan_int_rate": round(random.uniform(5.0, 30.0), 2),
        "loan_percent_income": round(random.uniform(0.05, 0.5), 2),
        "cb_person_cred_hist_length": random.randint(1, 30),
        "person_home_ownership": random.choice(["RENT", "OWN", "MORTGAGE", "OTHER"]),
        "loan_intent": random.choice(["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]),
        "loan_grade": random.choice(["A", "B", "C", "D", "E", "F", "G"]),
    }
    return application

# Function to simulate credit applications
def simulate_credit_applications(rate_per_minute=60, duration_minutes=10):
    total_applications = rate_per_minute * duration_minutes

    for _ in range(total_applications):
        application = generate_credit_application()

        try:
            response = requests.post(API_URL, json=application)
            if response.status_code == 200:
                result = response.json()
                print(f"Application: {application['loan_amnt']} - Credit Score: {result.get('credit_score', 'N/A')}")
            else:
                print(f"Failed to process application: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(60 / rate_per_minute)  # Wait before sending the next application

# API endpoint to trigger credit application simulation
@app.post("/simulate_credit_applications")
async def start_simulation(rate_per_minute: int = 60, duration_minutes: int = 10, background_tasks: BackgroundTasks = None):
    background_tasks.add_task(simulate_credit_applications, rate_per_minute, duration_minutes)
    return {"message": "Credit application simulation started", "rate_per_minute": rate_per_minute, "duration_minutes": duration_minutes}

# Run the server with: uvicorn credit_application_simulator_api:app --reload
