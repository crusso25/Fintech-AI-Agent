import pandas as pd
import joblib
import os
import numpy as np
from sklearn.metrics import accuracy_score

current_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(current_dir, 'models', 'fraud_model.pkl'))
scaler = joblib.load(os.path.join(current_dir, 'models', 'scaler.pkl'))

df = pd.read_csv('data/creditcard.csv')
df.rename(columns={'Time': 'TransactionTime', 'Amount': 'TransactionAmount', 'Class': 'FraudLabel'}, inplace=True)

features = ['TransactionTime', 'TransactionAmount'] + [f'V{i}' for i in range(1, 29)]
X = df[features]
y = df['FraudLabel']

X_sample = X.sample(n=1000000, replace=True, random_state=42)
y_sample = y.loc[X_sample.index]

X_scaled = scaler.transform(X_sample)

y_pred = model.predict(X_scaled)

y_pred_binary = np.where(y_pred == -1, 1, 0)  

accuracy = accuracy_score(y_sample, y_pred_binary)

correct_frauds = sum((y_sample == 1) & (y_pred_binary == 1))
missed_frauds = sum((y_sample == 1) & (y_pred_binary == 0))
false_positives = sum((y_sample == 0) & (y_pred_binary == 1))

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Correctly identified fraudulent transactions: {correct_frauds}")
print(f"Missed fraudulent transactions: {missed_frauds}")
print(f"Legitimate transactions falsely flagged as fraud: {false_positives}")
