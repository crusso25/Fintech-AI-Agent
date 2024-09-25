from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import socketio
from fastapi.middleware.cors import CORSMiddleware

# Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI(title="FinAI Integration API", version="1.0")
sio_app = socketio.ASGIApp(sio, app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class Transaction(BaseModel):
    # Fields expected by fraud_detection
    TransactionTime: float
    TransactionAmount: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

class CreditApplication(BaseModel):
    # Fields expected by credit_scoring
    person_age: int
    person_income: float
    person_emp_length: float
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: int
    person_home_ownership: str
    loan_intent: str
    loan_grade: str

# In-memory stores for recent transactions and applications
recent_transactions = []
recent_applications = []

# Endpoints

@app.post("/fraud_detection")
async def detect_fraud(transaction: Transaction):
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=transaction.dict()
        )
        response.raise_for_status()
        result = response.json()

        transaction_data = {
            'transaction_id': 'txn_' + str(len(recent_transactions) + 1), 
            'amount': transaction.TransactionAmount,
            'time': transaction.TransactionTime,
            'prediction': result['prediction'],
            'anomaly_score': result.get('probability', None)
        }
        # Store the transaction
        recent_transactions.insert(0, transaction_data)
        if len(recent_transactions) > 100:
            recent_transactions.pop()

        # Emit the result to connected clients
        await sio.emit('fraud_alert', transaction_data)

        return result
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/credit_scoring")
async def get_credit_score(application: CreditApplication):
    try:
        response = requests.post(
            "http://localhost:8001/credit_score", 
            json=application.dict()
        )
        response.raise_for_status()
        result = response.json()

        # Prepare data to emit
        application_data = {
            'application_id': 'app_' + str(len(recent_applications) + 1),
            'applicant_name': 'Applicant ' + str(len(recent_applications) + 1),
            'credit_score': result['credit_score'],
            'date': '2023-09-25'  # placeholder - USE CURRENT DATE WHEN PRODUCED
        }
        # Store the application
        recent_applications.insert(0, application_data)
        if len(recent_applications) > 100:
            recent_applications.pop()

        # Emit the result to connected clients
        await sio.emit('credit_score_update', application_data)

        return result
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FinAI Integration API"}

# Endpoint for recent fraudulent transactions
@app.get("/fraud_detection/recent")
async def get_recent_fraudulent_transactions():
    return {"transactions": recent_transactions}

# Endpoint for recent credit scoring results
@app.get("/credit_scoring/recent")
async def get_recent_credit_scores():
    return {"applications": recent_applications}

# Endpoint for system metrics (placeholder)
@app.get("/system_metrics")
async def get_system_metrics():
    # placeholder for monitoring
    metrics = [
        {
            "timestamp": "2023-09-25T12:00:00",
            "request_rate": 100,
            "response_time": 200
        },
    ]
    return {"metrics": metrics}

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(sio_app, host="0.0.0.0", port=8002)