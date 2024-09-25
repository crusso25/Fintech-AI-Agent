import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib
import os

df = pd.read_csv('data/creditcard.csv')
df.rename(columns={'Time': 'TransactionTime', 'Amount': 'TransactionAmount', 'Class': 'FraudLabel'}, inplace=True)


features = ['TransactionTime', 'TransactionAmount'] + [f'V{i}' for i in range(1, 29)]
X = df[features]
y = df['FraudLabel']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Model
model = IsolationForest(n_estimators=100, contamination=0.0017, random_state=42)
model.fit(X_scaled)

if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/fraud_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print("Model and scaler have been saved in the 'models' directory.")
