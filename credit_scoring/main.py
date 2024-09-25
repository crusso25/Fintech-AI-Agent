from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(current_dir, 'models', 'credit_model.pkl'))
scaler = joblib.load(os.path.join(current_dir, 'models', 'scaler.pkl'))
encoder = joblib.load(os.path.join(current_dir, 'models', 'encoder.pkl'))

class CreditApplication(BaseModel):
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

app = FastAPI(title="Credit Scoring API", version="1.0")

# Preprocess
def preprocess(application_data):
    # Convert to DF
    df = pd.DataFrame([application_data])

    categorical_features = ['person_home_ownership', 'loan_intent', 'loan_grade']
    numerical_features = [
        'person_age', 'person_income', 'person_emp_length',
        'loan_amnt', 'loan_int_rate', 'loan_percent_income',
        'cb_person_cred_hist_length'
    ]

    # Encode categorical variables
    df_encoded = pd.DataFrame(encoder.transform(df[categorical_features]))
    df_encoded.columns = encoder.get_feature_names_out(categorical_features)
    df_encoded.index = df.index
    df_numerical = pd.DataFrame(scaler.transform(df[numerical_features]), columns=numerical_features, index=df.index)
    df_processed = pd.concat([df_numerical, df_encoded], axis=1)

    return df_processed

# Prediction endpoint
@app.post('/credit_score')
def get_credit_score(application: CreditApplication):
    application_data = application.dict()
    try:
        processed_data = preprocess(application_data)
        score = model.predict_proba(processed_data)[:,1][0]  # Probability of default
        credit_score = int((1 - score) * 850)  # Scale to credit score range (0 to 850)
        return {'credit_score': credit_score}
    except Exception as e:
        return {'error': str(e)}

@app.get('/')
def read_root():
    return {'message': 'Welcome to the Credit Scoring API'}
