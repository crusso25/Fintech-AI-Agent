from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(current_dir, 'models', 'fraud_model.pkl'))
scaler = joblib.load(os.path.join(current_dir, 'models', 'scaler.pkl'))

class Transaction(BaseModel):
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

app = FastAPI()

@app.post('/predict')
def predict(transaction: Transaction):
    # Convert the Transaction object to a DataFrame
    transaction_df = pd.DataFrame([transaction.dict()])
    
    # Scale the features
    features = scaler.transform(transaction_df)
    
    # Predict
    prediction = model.predict(features)
    anomaly_score = model.decision_function(features)
    
    # Map the prediction to a readable format
    result = 'Fraudulent' if prediction[0] == -1 else 'Legitimate'
    
    # Since lower scores indicate anomalies, we can rescale anomaly scores to probabilities between 0 and 1
    # This is how we will scale the score:
    min_score = -0.5
    max_score = 0.5
    normalized_score = (anomaly_score[0] - min_score) / (max_score - min_score)
    probability = max(0, min(1, normalized_score))
    
    return {
        'prediction': result,
        'probability': float(probability)
    }